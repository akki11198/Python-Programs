stones = []
n = int(input())
for i in range(n):
    x = int(input())
    stones.append(x)
stones.sort()
s1, s2 = stones[-1], stones[-2]
while len(stones) > 1:
    if s1 == s2:
        stones.pop(-1)
        stones.pop(-1)
    else:
        s2 = abs(s1-s2)
        stones.pop(-1)
        stones[-1] = s2
if len(stones):
    print(stones[0])
else:
    print(0)
