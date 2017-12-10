
import sqlite3 as lite

cur = lite.connect('Stock.db')
con=cur.cursor()


class validator:
   def __init__(self):
      pass

   def validateAdd(self, array):
      self.array = array

      if type(array[1]) != int:
         print("")
         print("Item stock not valid type")
         return
      elif type(array[2]) != float:
         print("")
         print("Item price not valid type")
         return
      elif type(array[4]) != int:
         print("")
         print("Item Minimum not correct type")
         return
      elif type(array[5]) != int:
         print("")
         print("Item maximum not correct type")
         return
      else:
         verified = 1
         return verified
      
   def validateSale(self, array):
      self.array = array

      if type(array[0]) != int:
         print("")
         print("Incorrect ID")
      elif type(array[1]) != int:
         print("")
         print("Incorrect quantity type")
      else:
         print("Verified")
         
class userInput:
   def __init__(self):
      pass

   def userAdd(self):
      data=[]
      print("")
      ItemName = str(input("Enter Item name: "))
      ItemStock = input("Enter Item Stock: ")
      ItemPrice = input("Enter Item price '0.00 form': ")
      ItemArriveDate = input("Enter Date (as DD/MM/YYYY): ")
      ItemMinReq = input("Enter minimum required: ")
      ItemMaxReq = input("Enter maximum required: ")
      
      data = [ItemName, ItemStock, ItemPrice, ItemArriveDate, ItemMinReq, ItemMaxReq]
      Verified= validator.validateAdd(self, data)

      if Verified != 1:
         verify.verifyFalse(self)
         return

      data[1] = int(data[1])
      data[2] = float(data[2])
      data[4] = int(data[4])
      data[5] = int(data[5])

      data.append(Verified)
      return data

   def userSale(self):
      data = []
      print("")
      saleID = input("What is being sold? Enter ID: ")
      num = input("How many are being sold?: ")
      data = [saleID, num]
      validate.validateSale(self, data)
      
      data[0] = int(data[0])
      data[1] = int(data[1])
      return data
      
class event:
   def __init__(self, source, eventArguments):
      self.source = source
      self.eventArguments = eventArguments

class mediator:
   def __init__(self, subscriptions):
      self.subscriptions = subscriptions

   def eventLoop(self):
      for i in self.subscriptions:
         if i.source == "add":
            self.onAddEvent()
         elif i.source == "view":
            self.onViewEvent()
         elif i.source == "sale":
            self.onSaleEvent()
         
   def onAddEvent(self):
      data=[]
      data = userInput.userAdd(self)
      dataConvert.dataConvertTo(self, "add", data)
      verify.verifyTrue(self)

   def onViewEvent(self):
      data = []
      data = dataConvert.dataConvertFrom(self)
      for i in range(0, len(data)):
         print(str(data[i]).replace("(","").replace(")", ""))
      verify.verifyTrue(self)

   def onSaleEvent(self):
      data =[]
      data = userInput.userSale(self)
      dataConvert.dataConvertTo(self, "sale", data)
         
class dataConvert:
   def __init__(self):
      pass

   def dataConvertTo(self, calc, array):

      self.calc = calc
      self.array = array
      
      if calc == "add":
         
         toDatabase=[]
         name = str(array[0])
         stock = int(array[1])
         price = float(array[2])
         arrival = array[3]
         minReq = int(array[4])
         maxReq = int(array[5])
         real = int(array[6])
         toDatabase = [name, stock, price, arrival, minReq, maxReq, real]
         dataAccess.dataAccessAdd(self, toDatabase)
         return 
         
      elif calc == "sale":

         toDatabase=[]
         ID=int(array[0])
         num=int(array[1])
         toDatabase = [ID, num]
         
         sqlStuff = dataAccess.dataAccessGetSale(self, toDatabase)
         
         minimum = int(sqlStuff[0])
         maximum = int(sqlStuff[1])
         quantity = int(sqlStuff[2])

         sendToSql = []
         if num<maximum and num>minimum and num < quantity:
            quantity = quantity-num
            sendToSql = [ID, quantity]
            dataAccess.dataAccessUpdate(self, sendToSql)
            verify.verifyTrue(self)
            
         elif num>quantity:
            verify.verifyFalse(self)
            
         else:
            verify.verifyFalse(self)

   def dataConvertFrom(self):
      return(dataAccess.dataAccessGetView(self))

class dataAccess:
   def __init__(self):
      pass

   def dataAccessAdd(self, new):

      self.cur = lite.connect('Stock.db')
      self.con=self.cur.cursor()

      self.new = new
      
      item=1
      for row in self.con.execute("SELECT * FROM Items"):
              item+=1

      new.insert(0, item)
      
      self.con.execute("INSERT INTO Items VALUES (?,?,?,?,?,?,?,?)", new,)
      self.cur.commit()

      return
      
   def dataAccessGetView(self):
                       
      self.cur = lite.connect('Stock.db')
      self.con=self.cur.cursor()

      dataRetrieve=[]
      
      for row in self.con.execute("SELECT * FROM Items"):
         dataRetrieve.append(row)

      return dataRetrieve


   def dataAccessGetSale(self, new):
                       
      self.cur = lite.connect('Stock.db')
      self.con=self.cur.cursor()

      self.new = new
      array=[]

      ID = str(new[0])

      for row in self.con.execute("SELECT ItemID FROM Items"):
         array.append[i]

      if ID not in array:
         print("ID not valid")
         verify.verifyFalse(self)
         return

      self.con.execute("SELECT ItemMinReq FROM Items WHERE ItemID=?", ID,)
      minimum = self.con.fetchone()[0]

      self.con.execute("SELECT ItemMaxReq FROM Items WHERE ItemID=?", ID,)
      maximum = self.con.fetchone()[0]

      self.con.execute("SELECT ItemQuantity FROM Items WHERE ItemID=?", ID,)
      quantity = self.con.fetchone()[0]

      sqlData = [minimum, maximum, quantity]
      return sqlData
                 
   def dataAccessUpdate(self, new):
      self.cur = lite.connect('Stock.db')
      self.con=self.cur.cursor()

      self.new = new

      dataToInsert = []
      quantity=new[1]
      ID=new[0]
      dataToInsert = [quantity, ID]

      self.con.execute("UPDATE Items SET ItemQuantity=? WHERE ItemID=?", dataToInsert,)
      self.cur.commit()
      return
      
class verify:
   def __init__(self):
      pass

   def verifyTrue(self):
      print("")
      print("All done and working")
      print("")
      return

   def verifyFalse(self):
      print("")
      return
   
def main():
   while 1:
      mainList=[]
      Med = mediator(mainList)
      process = input("1 for add, 2 for view, 3 for sale: ")
      if process == "1":
         data = []
         mainList.append(event("add", data))
      elif process == "2":
         data=[]
         mainList.append(event("view", data))
      elif process == "3":
         data = []
         mainList.append(event("sale", data))
      else:
        print("Not valid, pick again")
        
      Med.eventLoop()
      
if __name__ == "__main__":
   main()
