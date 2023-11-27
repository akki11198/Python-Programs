n = int(input("Enter No of Rows : "))
m = int(input("Enter No of Columns : "))
Ar = []
out = []
print("Enter the " + str(n) + " * " + str(m) + " Array")
for i in range(n):
    c = []
    for j in range(m):
        t = int(input())
        c.append(t)
    Ar.append(c)
q = int(input("Enter the Number of Querries : "))
qrr = []
for i in range(q):
    g = []
    print("Enter Querry no " + str(i+1))
    for j in range(2):
        t = int(input())
        g.append(t)
    qrr.append(g)
for k in range(q):
    count = 0
    for i in range(n):
        ts = 0
        for j in range(m):
            ts = ts + Ar[i][j]
        if (qrr[k][0] <= ts <= qrr[k][1]):
            count = count+1

    for i in range(n):
        ts = 0
        for j in range(m):
            ts = ts + Ar[j][i]
        if (qrr[k][0] <= ts <= qrr[k][1]):
            count = count+1
    out.append(count)
for i in range(q):
    print("For Querry No " + str(i+1) + ", Sum of No of rows and Columns in the Range " +
          str(qrr[i][0]) + " and " + str(qrr[i][1]) + " is: " + str(out[i]))
