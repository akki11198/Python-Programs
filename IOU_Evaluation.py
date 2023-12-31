from __future__ import division
import os
import cv2
import numpy as np
import sys
import pickle
from optparse import OptionParser
import time
from keras_frcnn import config
from keras import backend as K
from keras.layers import Input
from keras.models import Model
from keras_frcnn import roi_helpers
import Intersection_Over_Union as iou
sys.setrecursionlimit(40000)

parser = OptionParser()

parser.add_option("-p", "--path", dest="test_path", help="Path to test data.")
parser.add_option("-o", "--parser", dest="parser", help="Parser to use. One of simple or pascal_voc",
                  default="pascal_voc")
parser.add_option("-n", "--num_rois", dest="num_rois",
                  help="Number of ROIs per iteration. Higher means more memory use.", default=16)
parser.add_option("--config_filename", dest="config_filename", help="Location to read the metadata related to the training (generated when training).",
                  default="config.pickle")
parser.add_option("--network", dest="network",
                  help="Base network to use. Supports vgg or resnet50.", default='vgg')

(options, args) = parser.parse_args()

if not options.test_path:   # if filename is not given
    parser.error(
        'Error: path to test data must be specified. Pass --path to command line')


config_output_filename = options.config_filename

with open(config_output_filename, 'rb') as f_in:
    C = pickle.load(f_in)

if options.network == 'vgg':
    C.network = 'vgg16'
    from keras_frcnn import vgg as nn
elif options.network == 'resnet50':
    from keras_frcnn import resnet as nn
    C.network = 'resnet50'
elif options.network == 'vgg19':
    from keras_frcnn import vgg19 as nn
    C.network = 'vgg19'
elif options.network == 'mobilenetv1':
    from keras_frcnn import mobilenetv1 as nn
    C.network = 'mobilenetv1'
#	from keras.applications.mobilenet import preprocess_input
elif options.network == 'mobilenetv1_05':
    from keras_frcnn import mobilenetv1_05 as nn
    C.network = 'mobilenetv1_05'
#	from keras.applications.mobilenet import preprocess_input
elif options.network == 'mobilenetv1_25':
    from keras_frcnn import mobilenetv1_25 as nn
    C.network = 'mobilenetv1_25'
#	from keras.applications.mobilenet import preprocess_input
elif options.network == 'mobilenetv2':
    from keras_frcnn import mobilenetv2 as nn
    C.network = 'mobilenetv2'
else:
    print('Not a valid model')
    raise ValueError

# turn off any data augmentation at test time
C.use_horizontal_flips = False
C.use_vertical_flips = False
C.rot_90 = False
i = 0
img_path = options.test_path


def bb_intersection_over_union(boxA, boxB):

    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    if((xB - xA) == 0 or (yB - yA) == 0):
        iou = 0.0
        return iou
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou


def format_img_size(img, C):
    """ formats the image size based on config """
    img_min_side = float(C.im_size)
    (height, width, _) = img.shape

    if width <= height:
        ratio = img_min_side/width
        new_height = int(ratio * height)
        new_width = int(img_min_side)
    else:
        ratio = img_min_side/height
        new_width = int(ratio * width)
        new_height = int(img_min_side)
    img = cv2.resize(img, (new_width, new_height),
                     interpolation=cv2.INTER_CUBIC)
    return img, ratio


def format_img_channels(img, C):
    """ formats the image channels based on config """
    img = img[:, :, (2, 1, 0)]
    img = img.astype(np.float32)
    img[:, :, 0] -= C.img_channel_mean[0]
    img[:, :, 1] -= C.img_channel_mean[1]
    img[:, :, 2] -= C.img_channel_mean[2]
    img /= C.img_scaling_factor
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    return img


def format_img(img, C):
    """ formats an image for model prediction based on config """
    img, ratio = format_img_size(img, C)
    img = format_img_channels(img, C)
    return img, ratio

# Method to transform the coordinates of the bounding box to its original size


def get_real_coordinates(ratio, x1, y1, x2, y2):

    real_x1 = int(round(x1 // ratio))
    real_y1 = int(round(y1 // ratio))
    real_x2 = int(round(x2 // ratio))
    real_y2 = int(round(y2 // ratio))

    return (real_x1, real_y1, real_x2, real_y2)


class_mapping = C.class_mapping

if 'bg' not in class_mapping:
    class_mapping['bg'] = len(class_mapping)

class_mapping = {v: k for k, v in class_mapping.items()}
# print(class_mapping)
class_to_color = {class_mapping[v]: np.random.randint(
    0, 255, 3) for v in class_mapping}
C.num_rois = int(options.num_rois)

if C.network == 'resnet50':
    num_features = 1024
elif C.network == "mobilenetv2":
    num_features = 320
else:
    # may need to fix this up with your backbone..!
    print("backbone is not resnet50. number of features chosen is 512")
    num_features = 512

if K.image_dim_ordering() == 'th':
    input_shape_img = (3, None, None)
    input_shape_features = (num_features, None, None)
else:
    input_shape_img = (None, None, 3)
    input_shape_features = (None, None, num_features)

img_input = Input(shape=input_shape_img)
roi_input = Input(shape=(C.num_rois, 4))
feature_map_input = Input(shape=input_shape_features)

# define the base network (resnet here, can be VGG, Inception, etc)
shared_layers = nn.nn_base(img_input, trainable=True)

# define the RPN, built on the base layers
num_anchors = len(C.anchor_box_scales) * len(C.anchor_box_ratios)
rpn_layers = nn.rpn(shared_layers, num_anchors)

classifier = nn.classifier(feature_map_input, roi_input,
                           C.num_rois, nb_classes=len(class_mapping), trainable=True)

model_rpn = Model(img_input, rpn_layers)
model_classifier_only = Model([feature_map_input, roi_input], classifier)

model_classifier = Model([feature_map_input, roi_input], classifier)

#print('Loading weights from {}'.format(C.model_path))
model_rpn.load_weights(C.model_path, by_name=True)
model_classifier.load_weights(C.model_path, by_name=True)

model_rpn.compile(optimizer='sgd', loss='mse')
model_classifier.compile(optimizer='sgd', loss='mse')

all_imgs = []

classes = {}

bbox_threshold = 0.8

visualise = True
iou_path = open(
    '/home/user/Desktop/Object_Detection/Code/frcnn-from-scratch-with-keras-master/mycords.txt', 'w+')
visualise = True
#path_Rect_txt = ''
fo = open('/home/user/Desktop/Object_Detection/Code/frcnn-from-scratch-with-keras-master/sampletest.txt', "r")
count = 0

for line in fo:
    line_split = line.strip().split(',')
    (filename, no_blocks, x_org, y_org, w_org, h_org, class_name) = line_split
# print(filename)
    # print((filename,x_org,y_org,w_org,h_org,class_name))
    # to know the name of file at index number
    img_name = (filename.strip().split('/'))[7]
    st = time.time()
    filepath = filename
    img = cv2.imread(filepath)
    X, ratio = format_img(img, C)
    p = img_name.split('.')
    p1 = p[0]
    if K.image_dim_ordering() == 'tf':
        X = np.transpose(X, (0, 2, 3, 1))

    # get the feature maps and output from the RPN
    [Y1, Y2, F] = model_rpn.predict(X)

    R = roi_helpers.rpn_to_roi(
        Y1, Y2, C, K.image_dim_ordering(), overlap_thresh=0.7)

    # convert from (x1,y1,x2,y2) to (x,y,w,h)
    R[:, 2] -= R[:, 0]
    R[:, 3] -= R[:, 1]

    # apply the spatial pyramid pooling to the proposed regions
    bboxes = {}
    probs = {}
    print("image=" + str(img_name))
    i = i+1
for jk in range(R.shape[0]//C.num_rois + 1):
    ROIs = np.expand_dims(R[C.num_rois*jk:C.num_rois*(jk+1), :], axis=0)
    if ROIs.shape[1] == 0:
        break

    if jk == R.shape[0]//C.num_rois:
        # pad R
        curr_shape = ROIs.shape
        target_shape = (curr_shape[0], C.num_rois, curr_shape[2])
        ROIs_padded = np.zeros(target_shape).astype(ROIs.dtype)
        ROIs_padded[:, :curr_shape[1], :] = ROIs
        ROIs_padded[0, curr_shape[1]:, :] = ROIs[0, 0, :]
        ROIs = ROIs_padded

    [P_cls, P_regr] = model_classifier_only.predict([F, ROIs])

    for ii in range(P_cls.shape[1]):

        if np.max(P_cls[0, ii, :]) < bbox_threshold or np.argmax(P_cls[0, ii, :]) == (P_cls.shape[2] - 1):
            continue

        cls_name = class_mapping[np.argmax(P_cls[0, ii, :])]

        if cls_name not in bboxes:
            bboxes[cls_name] = []
            probs[cls_name] = []

        (x, y, w, h) = ROIs[0, ii, :]

        cls_num = np.argmax(P_cls[0, ii, :])
        try:
            (tx, ty, tw, th) = P_regr[0, ii, 4*cls_num:4*(cls_num+1)]
            tx /= C.classifier_regr_std[0]
            ty /= C.classifier_regr_std[1]
            tw /= C.classifier_regr_std[2]
            th /= C.classifier_regr_std[3]
            x, y, w, h = roi_helpers.apply_regr(x, y, w, h, tx, ty, tw, th)
        except:
            pass
        bboxes[cls_name].append(
            [C.rpn_stride*x, C.rpn_stride*y, C.rpn_stride*(x+w), C.rpn_stride*(y+h)])
        probs[cls_name].append(np.max(P_cls[0, ii, :]))

all_dets = []
prob = 0
prob_cordinate = [0, 0, 0, 0]
# print(bboxes)
for key in bboxes:
    #print("key=" + str(key))
    bbox = np.array(bboxes[key])
    new_boxes, new_probs = roi_helpers.non_max_suppression_fast(
        bbox, np.array(probs[key]), overlap_thresh=0.5)
    new_probs = list(new_probs)
    #print(new_boxes, new_probs)
    max_prob = max(new_probs)
    element_index = new_probs.index(max_prob)
    if(max_prob > prob):
        prob = max_prob
        prob_cordinate = new_boxes[element_index, :]
    count = count+1
    (x1, y1, x2, y2) = prob_cordinate
    # print(prob_cordinate)
    # print(ratio)
    (x1_p, y1_p, x2_p, y2_p) = get_real_coordinates(ratio, x1, y1, x2, y2)
    x1_org = int(x_org)
    y1_org = int(y_org)
    x2_org = int(w_org)
    y2_org = int(h_org)

    ground_truth_box = [x1_org, y1_org, x2_org, y2_org]
    predict_box = [x1_p, y1_p, x2_p, y2_p]
    cv2.rectangle(img, (x1_org, y1_org,), (y2_org, x2_org), (255, 255, 0), 2)
    #cv2.rectangle(img,(x1_p, y1_p), (x2_p, y2_p), (255, 0, 0),3)
    print("GROUNDTRUTH=" + str(ground_truth_box))
    #print("Predicted=" + str(predict_box))
    # print(IOU)
    cv2.imwrite(
        '/home/user/Desktop/Object_Detection/Code/frcnn-from-scratch-with-keras-master/test/' + img_name, img)
    # Find Intersection over Union
    IOU = abs(iou.bb_intersection_over_union(ground_truth_box, predict_box))
cv2.putText(img, "IoU: {:.4f}".format(IOU), (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
iou_path.write(str(IOU) + "\n")
print(IOU)
print("{}".format("IOU") + str(IOU))
