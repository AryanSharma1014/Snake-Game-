print("-------BODY MASS INDEX-------")
print("Welcome..please input your details that are asked for ur BMI calculation!!!")
weight = float(input("Enter your weight (in kg):"))
height = float(input("Enter your height (in m):"))

BMI = weight / (height**2)
print(f"\n your BMI is: {BMI:.2f}")
if BMI < 18.5:
    print("You are underweight.")
elif 18.5 <= BMI < 24.9:
    print("You have a normal weight.")
elif 25 <= BMI < 29.9:
    print("You are overweight.")
else:
    print("You are obese.")