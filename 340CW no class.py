import sqlite3 as lite

cur = lite.connect('Stock.db')
con=cur.cursor()

'''adding'''

ItemName = str(input("Enter Item name: "))
ItemStock = int(input("Enter Item Stock: "))
ItemPrice = float(input("Enter Item price '0.00 form': "))
ItemArriveDate = input("Enter Date (as DD/MM/YYYY): ")
ItemMinReq = int(input("Enter minimum required: "))
ItemMaxReq = int(input("Enter maximum required: "))
Verified= int(input("1 for verify, 0 for not: "))

item=1
for row in con.execute("SELECT * FROM Items"):
        item+=1

new = [item, ItemName, ItemStock, ItemPrice, ItemArriveDate, ItemMinReq, ItemMaxReq, Verified]
con.execute("INSERT INTO Items VALUES (?,?,?,?,?,?,?,?)", new)
cur.commit()


'''view'''

for row in con.execute("SELECT * FROM Items"):
   print(row)

'''sale'''

saleID = input("What is being sold? Enter ID: ")
num = int(input("How many are being sold?: "))

con.execute("SELECT ItemMinReq FROM Items WHERE ItemID=?", saleID,)
minimum = con.fetchone()[0]

con.execute("SELECT ItemMaxReq FROM Items WHERE ItemID=?", saleID,)
maximum = con.fetchone()[0]

con.execute("SELECT ItemQuantity FROM Items WHERE ItemID=?", saleID,)
quantity = con.fetchone()[0]
   
if num<maximum and num>minimum and num < quantity:
   quantity = quantity-num
   con.execute("UPDATE Items SET ItemQuantity=? WHERE ItemID=?", (quantity, saleID,))
   cur.commit()
elif num>quantity:
   print("Nah Mate. Not enough innit")
else:
   print("Woops, too much. too little. ask for in range next time")

