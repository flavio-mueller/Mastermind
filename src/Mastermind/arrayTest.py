arr = [[None for _ in range(4)] for _ in range(1296)]
i = 0


for x in range(0, 6):
    for y in range(0, 6):
        for z in range(0, 6):
            for j in range(0, 6):
                arr[i][0] = x
                arr[i][1] = y
                arr[i][2] = z
                arr[i][3] = j
                i += 1

print(len(arr))
k = arr[5]
del(arr[5])
print(len(arr))
print(k)