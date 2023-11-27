n = int(input())
strn = []

for i in range(n):
    x = input()
    strn.append(x)
for i in strn:
    s1 = []
    s2 = []
    s = len(i)
    for j in range(s):
        if (j % 2 == 0):
            s1.append(strn[i][j])
        elif (j % 2 != 0):
            s2.append(strn[i][j])
    print(str(s1)+" "+str(s2))
