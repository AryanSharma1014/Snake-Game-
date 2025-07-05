a= float(input("a:"))
b= float(input("b:"))
operation=input("enter the operation:+,-,*,/:")
if operation == "+":
    result= a+b
    print("sum of a+b:",result)
elif operation == "-":
    result= a-b
    print("difference of a-b:",result)
elif operation == "*":
    result = a*b  
    print("product of a and b:",result)
elif operation == "/":
    if b==0:
        print("undefined value")
    else:
        result= a/b
        print("result of a/b:",result)
else:
    print("invalid operation")                     