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
# I decided on the values based on imprtance of each field by research, and by comparing fields to each other based on the number of edge cases. 
# e.g. A user with many years of experience but a low no of previous clients is still good. 
# Meaning years experince is significantly more important that no of previous clients on the app.
# For some fields, the differnce between values is not that important. If these fields need to be used to affect other values 
# (e.g. ) num previous clients determines whether the days since last logon is a red flag. But we only need to know whether they have 0 previous clients. 
# Becuase if the nad no previous clients, and havent logged on in moths, they are a much worse fit that someone who has at least had a client, no matter how long ago they logged on

# REMOVE EXTRA UNNORMALISED VARIABLES IF NOT NEEDED


### Start of program ###
from numpy.core.numeric import tensordot
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
min_max_scaler = preprocessing.MinMaxScaler() #create a scaler object
years_exp = np.array(carer_data['years_experience']).reshape((len(carer_data['years_experience']), 1)) # extract years experience column and make it a 2d list/array
n_years_exp = min_max_scaler.fit_transform(years_exp)*100 # fit and then normalise values, and then multiply by 100 to get score
print("\n\nNormalised Years experience: \n")
print(n_years_exp)

# AVERAGE REVIEW
# Extract and modify according to the number of reviews, i.e. if the number of reviews are 0, take one point off. Then normalise data
avg_num_reviews = np.array(carer_data[['num_reviews','avg_review']]) # extract years experience column and make it a 2d list/array
avg_num_reviews[avg_num_reviews[:, 0] == 0, 1] = avg_num_reviews[avg_num_reviews[:, 0] == 0, 1] - 1 # if the number of reviews is 0, reduce the average review score by 1 point
print("\n\nAverage and number of review ")
print(avg_num_reviews)
n_average_rev = min_max_scaler.fit_transform(np.array(avg_num_reviews[:, 1]).reshape((len(avg_num_reviews[:, 1]), 1)))*100 # fit and then normalise values, and then multiply by 100 to get score
print("\n\nNormalised Average review ")
print(n_average_rev)

# NUMBER OF PREVIOUS CLIENTS
# Extract and normalise data
# # This has less of an impact becuase say they have 0 previous clients but have 20 years experience, they are still very suited! but experience through the app is still important 
# because the brand may require different things, and it is more reliable
num_prev_clients = np.array(carer_data['num_previous_clients']).reshape((len(carer_data['num_previous_clients']), 1)) # extract no previous clients column and make it a 2d list/array
n_num_previous_cli = min_max_scaler.fit_transform(num_prev_clients)*50 # fit and then normalise values, and then multiply by 50 to get score
print("\n\nNumber of Previous Clients: \n")
print(n_num_previous_cli)

# DAYS SINCE LAST LOGON
# Extract data, and modify according to the number of previous clients to create a greater disparity between those who have logged in a while ago due to having current clients, 
# and those who have had no clients and signed up for the banter
days_since_log = np.array(carer_data['days_since_login']) # extract days since logon
mean_login = np.mean(days_since_log) # get average logon time
three_quart_percentile = np.percentile(days_since_log, 75) # get lower percentile logon time
print("\n\nMean login time is ")
print(mean_login)
print("\n\n75 percent login time is ")
print(three_quart_percentile)
days_prev_clients = np.array(carer_data[['num_previous_clients', 'days_since_login']])
days_prev_clients[np.logical_and(days_prev_clients[:, 0] == 0, days_prev_clients[:, 1] > mean_login, days_prev_clients[:, 1] <= three_quart_percentile), 1] = days_prev_clients[np.logical_and(days_prev_clients[:, 0] == 0, days_prev_clients[:, 1] > mean_login, days_prev_clients[:, 1] <= three_quart_percentile), 1] * 2 # if no of previous clients is 0, make the days since last login half if it is greater than the average
days_prev_clients[np.logical_and(days_prev_clients[:, 0] == 0, days_prev_clients[:, 1] > three_quart_percentile), 1] = days_prev_clients[np.logical_and(days_prev_clients[:, 0] == 0, days_prev_clients[:, 1] > three_quart_percentile), 1] *4 # if no of previous clients is 0, make the days since last login a quarter if it is greater than the quarter
print("\n\n Number previous clients and Days since last login : ")
print(days_prev_clients)
n_days_since_log = (1-min_max_scaler.fit_transform(days_prev_clients[:, 1].reshape(len(days_prev_clients[:, 1]),1))) * 25
print("\n\nNormalised Days since last logon")
print(n_days_since_log)

# IMAGE PROBLEMS
img_problems = num_prev_clients = np.array(carer_data['img_problems']).reshape((len(carer_data['img_problems']), 1))
n_image_probs = (1-min_max_scaler.fit_transform(img_problems)) * 25
print("\n\nNormalised Image Problems")
print(n_image_probs)

#combine all the arrays together to make a big scoreboard
#scores = [n_years_exp, n__average_rev, n_num_previous_cli, n_days_since_log, n_image_probs]
score_board = np.hstack((np.array(carer_data[['id', 'first_name', 'last_name', 'num_reviews', 'avg_review', 
'img_problems','type','num_previous_clients','days_since_login', 'age', 'years_experience']]), n_years_exp, n_average_rev, n_num_previous_cli, n_days_since_log, n_image_probs)) # create large scoreboard with individual scores for each field
print("\n\n\nScore_board")
print(score_board)

#From this, calculate the total score and sort by score
sum_scores = score_board[:,11] + score_board[:,12] + score_board[:,13] + score_board[:,14] + score_board[:,15]  # add all the scores together
score_board = np.c_[score_board, sum_scores] # append the total on the end of the scoreboard (for checking reasons)
sorted_scores = score_board[np.argsort(sum_scores)][::-1] # sort the carers by total score
print("\n\n\n FINAL SORTED SCORES")
print(sorted_scores)
sorted_scores = np.vstack((['id', 'first_name', 'last_name', 'num_reviews', 'avg_review', 
'img_problems','type','num_previous_clients','days_since_login', 'age', 'years_experience', "total_score"], sorted_scores[:, [0,1,2,3,4,5,6,7,8,9,10,16]]))
np.savetxt("Best_carers_scoresheet.csv", sorted_scores, delimiter=",", fmt="%s") # save final scores in file
