def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)


x = int(input("Enter a number: "))
for i in range(0, x+1):
    print(fibonacci(i))
