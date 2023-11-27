
def MxMn(arr, n, k):
    maxOfMin = -9999
    z = []
    for i in range(n - k + 1):
        min = arr[i]
        for j in range(k):
            if (arr[i + j] < min):
                min = arr[i + j]
        if (min > maxOfMin):
            maxOfMin = min
        z.append(maxOfMin)
    z.sort()
    x = z[-1]
    return x


n = int(input("Enter The Number of Elements : "))
k = int(input("Enter the Window Size : "))
arr = []
print("Enter Array Elements :")
for i in range(n):
    z = int(input())
    arr.append(z)
ans = MxMn(arr, n, k)
print("The Max of Mins In the Array with Window Size is " +
      str(k) + " is: " + str(ans))
