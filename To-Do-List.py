tasks=[]
while True:
    print("\n1.ADD TASK\n2.VIEW Task\n3.REMOVE Task\n4.EXIT")
    choice=input("choose:")

    if choice == "1":
        task = input("Enter Task:")
        tasks.append(task)
        print("Your Task is added..")
    elif choice == "2":
        for i,task in enumerate(tasks,1):
            print(f"{i}.{task}")
    elif choice == "3":
        num=int(input("Enter the task you want to delete/remove:"))
        if 1<=num <=len(tasks):
            removed = tasks.pop(num-1)
            print(f"removed:{removed}")
        else:
            print("you input wrong number!!!!!input valid task number!!!")
    elif choice =="4":
        print("you select exit option!!")
        break     
    else:
        print("Invalid number!! Provide valid number from list!!!!")   