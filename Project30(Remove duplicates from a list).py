list = [1,1,1,1,2,3,3,3,4,4,5,5,6,6,7,8,8,8,9,9,10,10]

un = []

for i in list:
    if i not in un:
        un.append(i)

print(un)