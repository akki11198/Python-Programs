# a program to find the prime numbers
def prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


x = int(input("Enter a number: "))
if prime(x):
    print("Prime")
else:
    print("Not Prime")
    