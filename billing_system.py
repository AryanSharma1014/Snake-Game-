print("THIS IS THE BILL OF YOUR SHOPPING!!!")
items = []
while True:
    name= input("Enter item name:")
    price=float(input("Enter the price(rs):"))
    quantity=int(input("Quantity of item purchased:"))
    items.append({
    'name':name,
    'price':price,
    'quantity':quantity,
    'total':price*quantity
   })        
    more= input("Want to shop more??->(yes/no):").lower()
    if more != "yes":
        break
print("============BILL============")
grand_total = 0
for item in items:
    print(f"{item['name']} (rs{item['price']} x {item['quantity']}) = rs{item['total']}")
    grand_total += item['total']
gst_rate =0.18 
print("gst rate is 18%!!")
gst = grand_total*gst_rate
final_amount = grand_total + gst
print("------------------------------")
print(f"Total (Before GST): rs{grand_total:.2f}")
print(f"GST @18% : rs{gst:.2f}")
print(f"Final Amount: rs{final_amount:.2f}")
print("THANK YOU FOR YOUR KIND VISIT")
print("===============================")