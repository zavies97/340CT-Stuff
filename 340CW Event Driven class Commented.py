'''Imports the SQL library into python,
to be able to use SQl to connect to the database'''
import sqlite3 as lite

'''This class validates all data entered by the user.
As the data follows strict rules, the validator checks the data to
these rules to determine whether it is correct or not.
This applies to two different events: Add and Sale'''
class validator:
   def __init__(self):
      pass

   #Validates the data to add into the database
   def validateAdd(self, array):
      self.array = array

      verified = 0

      #If the entered data is not the correct type,
      #an error is thrown and the process closes
      #after alerting the user that the process failed
      try:
         int(array[1])
      except:
         print("")
         print("item stock not valid type")
         return verified

      try:
         float(array[2])
      except:
         print("")
         print("Item price not valid type")
         return verified

      try:
         int(array[4])
      except:
         print("")
         print("Item Minimum not correct type")
         return verified

      try:
         int(array[5])
      except:
         print("")
         print("Item maximum not correct type")
         return verified
      
      #If all the data is the correct type, the data
      #is officially verified and the verify code is sent
      #back to the userInput class
      verified = 1
      return verified
   
   #Validates the data to be used to update the database
   def validateSale(self, array):
      self.array = array

      verified = 0
      #If the entered data is not the correct type,
      #an error is thrown and the process closes
      #after alerting the user that the process failed
      try:
         int(array[0])
      except:
         print("")
         print("Incorrect ID")
         return verified

      try:
         int(array[1])
      except:
         print("")
         print("Incorrect quantity type")
         return verified

      verified = 1
      print("")
      print("Verified")
      return verified

'''This class manages the users input.
It is called for the add and sale events and relates to the
validation class once the data is entered'''  
class userInput:
   def __init__(self):
      pass

   #User specifies what to add to the database here
   def userAdd(self):
      data=[]
      print("")
      ItemName = input("Enter Item name: ")
      ItemStock = input("Enter Item Stock: ")
      ItemPrice = input("Enter Item price '0.00 form': ")
      ItemArriveDate = input("Enter Date (as DD/MM/YYYY): ")
      ItemMinReq = input("Enter minimum required: ")
      ItemMaxReq = input("Enter maximum required: ")

      #The data to add is stored in the list 'data' to be sent to the validator.
      #This validates the data and subsequently verifies whether it is real data
      #If it isnt, the program returns an error and the program resets.
      #If it is, the data is returned to be converted.
      data = [ItemName, ItemStock, ItemPrice, ItemArriveDate, ItemMinReq, ItemMaxReq]
      Verified= validator.validateAdd(self, data)

      if Verified != 1:
         data.append(Verified)
         return data

      data[0] = str(data[0])
      data[1] = int(data[1])
      data[2] = float(data[2])
      data[4] = int(data[4])
      data[5] = int(data[5])
      data.append(Verified)
      return data

   #User specifies what to update in the database
   #(what has been sold)
   def userSale(self):
      data = []
      print("")
      saleID = input("What is being sold? Enter ID: ")
      num = input("How many are being sold?: ")

      #The data to update is stored in the list 'data' to be sent to the validator.
      #This validates the data and subsequently verifies whether it is real data
      #If it isnt, the program returns an error and the program resets.
      #If it is, the data is returned to be converted.      
      data = [saleID, num]
      Verified = validator.validateSale(self, data)

      if Verified != 1:
         data.append(Verified)
         return data
      
      data[0] = int(data[0])
      data[1] = int(data[1])
      return data

'''This class tells the mediator what event to call'''
class event:
   def __init__(self, source, eventArguments):
      self.source = source
      self.eventArguments = eventArguments

'''This class maintains the processes needed to complete the events'''
class mediator:
   def __init__(self, subscriptions):
      self.subscriptions = subscriptions

   #Decides which event needs to be carried out
   def eventLoop(self):
      for i in self.subscriptions:
         if i.source == "add":
            self.onAddEvent()
         elif i.source == "view":
            self.onViewEvent()
         elif i.source == "sale":
            self.onSaleEvent()

   #Starts the Add event processes, first being accessing the
   #user input class to get the data, then validating said data,
   #then converting the data, then accessing the database to
   #insert the data and finally verifying it.
   def onAddEvent(self):
      data=[]
      data = userInput.userAdd(self)
      if data[6] != 1:
         verify.verifyFalse(self)
         return
      dataConvert.dataConvertTo(self, "add", data)
      verify.verifyTrue(self)

   #Starts the View event processes, first being accessing the database
   #to collect the data, then converting the data
   #and finally verifying it outputting the data.
   def onViewEvent(self):
      data = []
      data = dataConvert.dataConvertFrom(self)
      for i in range(0, len(data)):
         print(str(data[i]).replace("(","").replace(")", ""))
      verify.verifyTrue(self)

   #Starts the Sale event processes, first being accessing the
   #user input class to get the data, then validating said data,
   #then accessing the database to get data,
   #then converting the data from the database and from the user,
   #then accessing the database to update the data and finally verifying it.
   def onSaleEvent(self):
      data =[]
      data = userInput.userSale(self)
      if data[2] != 1:
         verify.verifyFalse(self)
         return
      dataConvert.dataConvertTo(self, "sale", data)

'''This class converts the data to its relevant form.
It acts as a midway class between the database and the users data,
converting data from the database into strings, integers and floats
to be used in calculations, and converting the users data to the same
types to be accepted into the database'''
class dataConvert:
   def __init__(self):
      pass

   #Converts the data to the relevant format to insert
   #into the database. It takes two arguments: calc and array
   #where calc is the operation to be done and array is the
   #list of data to be converted
   def dataConvertTo(self, calc, array):

      self.calc = calc
      self.array = array

      #if the operation is to add, the add data is converted into
      #its relevant format and sent to the data access class to
      #be inserted into the database
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

      #if the operation is the sale, the data from the relevant ID
      #is collected from the database. This data is the quantity
      #minimum required amount and maximum required amount.
      #After this data is collected, it is compared to the
      #sold amount. If it is within the right range, the sale continues and
      #the sales data is converted into its relevant format and sent to the
      #data access class to update the database.
      #Otherwise an error occurs and the process ends.
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
            return
            
         elif num>quantity:
            print("")
            print("Too much sold")
            verify.verifyFalse(self)
            return
            
         else:
            print("")
            print("Too little sold")
            verify.verifyFalse(self)
            return

   #Converts the data to the relevant format when retrieving
   #fromt the database. This function is just a middle step
   #between the database and viewing the data from the database
   def dataConvertFrom(self):
      return(dataAccess.dataAccessGetView(self))

'''This class accesses data from the database.
It is used to collect data from the database for the sale and
view events, as well as insert data into the database or the
add and sale events.'''
class dataAccess:
   def __init__(self):
      pass

   #Uses the data from the conversion stage to add to the database
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

   #Extracts all the data from the dtaabase and stores it in an array.
   #This data is then sent back to the mediator to be sent to the
   #user input class to be printed in the correct format.
   def dataAccessGetView(self):
                       
      self.cur = lite.connect('Stock.db')
      self.con=self.cur.cursor()

      dataRetrieve=[]
      
      for row in self.con.execute("SELECT * FROM Items"):
         dataRetrieve.append(row)

      return dataRetrieve

   #Extracts the relevant data for the requested ID. This data is then
   #used to determine whether the sale is possible or not.
   #It is stored in an array to be sent back to the data converter
   def dataAccessGetSale(self, new):
                       
      self.cur = lite.connect('Stock.db')
      self.con=self.cur.cursor()

      self.new = new

      ID = str(new[0])

      item=1
      for row in self.con.execute("SELECT * FROM Items"):
         item+=1

      if int(ID) > item:
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

   #Updates the data for the relevant ID after it has been approved.
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

'''This class verifies that the event is complete or not and prints
the relevant response.'''  
class verify:
   def __init__(self):
      pass

   #Shows the user that the data is all verified
   def verifyTrue(self):
      print("")
      print("All done and working")
      print("")
      return

   #Ends the process, the error code is stated as this function is called
   def verifyFalse(self):
      print("")
      return

'''This function is the main basis of the code.
Whne the program starts, this process is called.
When an event is chosen, a signal is sent to the mediator and the event
begins. Once the event ends, the process repeats until a new event
is chosen.'''
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
