st1 = input()
st2 = reversed(st1)
print(st2)
if list(st1) == list(st2):
    print("String is Palindrome")
else:
    print("String Not A Palindrome")
