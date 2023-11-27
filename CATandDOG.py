def chk(seq, c, d, ac):
    dgs = seq.count('d')
    dg_ate = 0
    for i in range(len(seq)):
        if (seq[i] == 'c' or seq[i] == 'C'):
            if c <= 0:
                break
            c = c-1
        else:
            if d <= 0:
                break
            d = d-1
            dg_ate = dg_ate + 1
            c = c + ac
    if dg_ate == dgs:
        return "NO"
    else:
        return "YES"


n = int(input("Total Animals: "))
d = int(input("No. of Dog FOOD: "))
c = int(input("No. of Cat FOOD: "))
ac = int(input("Additional Cat Food: "))
seq = input("Enter the Feeding ORDER: ")
ans = chk(seq, c, d, ac)
print(ans)
