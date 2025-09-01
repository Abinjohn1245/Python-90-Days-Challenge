numbers = [2, 3, 2, 5, 3, 2]

frequency = {}

for num in numbers:
    if num in frequency:
        frequency[num] += 1
    else:
        frequency[num] = 1

print("Frequencies:")

for k, v in frequency.items():
  print(k,v)