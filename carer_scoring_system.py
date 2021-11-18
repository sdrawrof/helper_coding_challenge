####  Some practice code (delete!)  ####

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

##### Notes to organise later! ######
# The fields included as values are all independent, and the rest of the fields are dependent on these ones
# #I decided on the values based on imprtance of each field by comparing fields to each other based on the number of edge cases. 
# e.g. A user with many years of experience but a low no of previous clients is still good. 
# Meaning years experince is significantly more important that no of previous clients on the app.
# For some fields, the differnce between values is not that important. If these fields need to be used to affect other values 
# (e.g. ) num previous clients determines whether the days since last logon is a red flag. But we only need to know whether they have 0 previous clients. 
# Becuase if the nad no previous clients, and havent logged on in moths, they are a much worse fit that someone who has at least had a client, no matter how long ago they logged on


### Start of program ###
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

#import carers data from csv file
carer_data = pd.read_csv('data.csv')
#print(carer_data)p
#print(carer_data['first_name'][0])
#for i in carer_data.index:
#    print(carer_data['first_name'][i])

# YEARS OF EXPERIENCE
# Extract and normalise data
min_max_scaler = preprocessing.MinMaxScaler()
n_years_exp = min_max_scaler.fit_transform(carer_data['years_experience'].to_numpy().tolist()) # extract years experience column
print(n_years_exp)