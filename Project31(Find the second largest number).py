numbers = [10, 3, 5, 2, 8,56,7,8,5,7,78,54,45,56,46,46,66,65,66,67]

n = len(numbers)
for i in range(n):
    for j in range(0, n - i - 1):
        if numbers[j] < numbers[j + 1]:
            numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]  # Swap

print("Second largest number :", numbers[1])
