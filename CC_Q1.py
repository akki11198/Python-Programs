t = int(input())
strs = []
for i in range(t):
    s = input()
    strs.append(s)
for i in strs:
    arr = list(i)
    eng = arr.count('2')
    ind = arr.count('1')
    drw = arr.count('0')
    if(eng == ind):
        print("DRAW")
    elif(eng > ind):
        print("ENGLAND")
    elif(ind > eng):
        print("INDIA")
