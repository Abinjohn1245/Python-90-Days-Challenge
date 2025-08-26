numbers = [1, 2, 3]
to_remove = int(input("Enter number to remove: "))

if to_remove in numbers:
    numbers.remove(to_remove)
    print("Updated list:", numbers)
else:
    print("Number not found in the list")

