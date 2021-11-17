#some practice code (delete!)
#print("Hello World")
#testList = ["princess", "beverley"]
#print("Test list is " + testList[0])

#myTuple = ("asparagus", "bottle", "carrot")
#print("Tuple is " + str(myTuple))

#thisdict = {
#  "brand": "Ford",
#  "model": "Mustang",
#  "year": 1964
#}
#print("This dictionary is " + str(thisdict))
#print(thisdict["year"])

#Import the csv file data
import pandas as pd

#import carers data from csv file
carer_data = pd.read_csv('data.csv')
#print(carer_data)
#print(carer_data['first_name'][0])

for i in carer_data.index:
    print(carer_data['first_name'][i])
