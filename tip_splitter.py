print("Welcome to the Tip Splitter App!")
bill_amount = float(input("Enter the total bill amount (₹): "))
tip_percent = float(input("Enter the tip percentage (%): "))
people = int(input("How many people to split the bill with? "))
tip_amount = bill_amount * (tip_percent / 100)
total_amount = bill_amount + tip_amount
per_person = total_amount / people
print("\n----- BILL SUMMARY -----")
print(f"Bill Amount     : ₹{bill_amount:.2f}")
print(f"Tip Amount      : ₹{tip_amount:.2f}")
print(f"Total with Tip  : ₹{total_amount:.2f}")
print(f"Each Person Pays: ₹{per_person:.2f}")
