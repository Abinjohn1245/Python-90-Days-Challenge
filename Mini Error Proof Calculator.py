def error_proof_calculator():
    print("=== Error-Proof Calculator ===")
    print("Available operations: +, -, *, /")
    
    while True:
        try:
            num1 = float(input("\nEnter first number: "))
            num2 = float(input("Enter second number: "))
            op = input("Enter operator (+, -, *, /): ")

            if op == "+":
                result = num1 + num2
            elif op == "-":
                result = num1 - num2
            elif op == "*":
                result = num1 * num2
            elif op == "/":
                if num2 == 0:
                    print("Error: Division by zero is not allowed.")
                    
                result = num1 / num2
            else:
                print("Invalid operator! Please try again.")
                

            print(f"Result: {result}")

        except Exception as e:
            print(f"Unexpected error: {e}")

        choice = input("\nDo you want to calculate again? (yes/no): ").lower()
        if choice != "yes":
            print("Calculator closed.")
            break


error_proof_calculator()
