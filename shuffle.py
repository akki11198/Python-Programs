#Shuffle contents of a list in fixed indexes.
a = ['a','b','c','d','e','f','g','h','i','j']
s1 = [2,4,7,5,0]
s2=[1,3,6,8,9]    #s1 and s2 are the indexes of the list a

for i in range(len(s1)):
    if i < len(s1)-1:
        a[s1[i]], a[s1[i+1]] = a[s1[i+1]], a[s1[i]]
    else:
        a[s1[i]], a[s1[0]] = a[s1[0]], a[s1[i]]

print(a)