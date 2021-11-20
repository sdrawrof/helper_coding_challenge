# 
# Written by Adia-May Macheny for the Helper.Community Coding Challenge
# 
# Two Errors in the data were identified. There were:
#  1. Some carers have an average review despite number of reviews being zero.
#     To reduce the impact of this on data I reduce carers with no reviews by
#     1 star,
#     although in relaity this may need to be mdofied further.
#  2. Number of reviews is sometimes higher than number of previous clients.
#
# 
#  #### Notes to organise later! ######
# The fields included as values are all independent, and the rest of the fields
#  are dependent on these ones
# I decided on the values based on imprtance of each field by research, and by
# comparing fields to each other based on the number of edge cases.
# e.g. A user with many years of experience but a low no of previous clients is
#  still good.
# Meaning years experince is significantly more important that no of previous
#  clients on the app.
# For some fields, the differnce between values is not that important. If these
#  fields need to be used to affect other values
# (e.g. ) num previous clients determines whether the days since last logon is
# a red flag. But we only need to know whether they have 0 previous clients.
# Becuase if the nad no previous clients, and havent logged on in moths, they
# are a much worse fit that someone who has at least had a client, no matter
#  how long ago they logged on

# REMOVE EXTRA UNNORMALISED VARIABLES IF NOT NEEDED


import pandas as pd
import numpy as np
from numpy.core.numeric import tensordot
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler


class CarerScorer:
    carer_data = pd.read_csv("data.csv")
    min_max_scaler = preprocessing.MinMaxScaler()

    # YEARS OF EXPERIENCE
    # Years of experience are converted into a score out of 100
    def calc_years_experience(self):
        # extract years_experience column
        years_exp = np.array(self.carer_data['years_experience']).reshape(
            (len(self.carer_data['years_experience']), 1))
        # fit and then normalise values, then * 100 for score
        n_years_exp = self.min_max_scaler.fit_transform(years_exp) * 100
        print(np.ndim(n_years_exp))
        return(n_years_exp)

    # AVERAGE REVIEW
    # Scored out of 100. See above notes for mitigation for users with zero number of reviews
    def calc_average_review(self):
        # extract average reviews and number of reviews columns
        avg_num_reviews = np.array(self.carer_data[['num_reviews', 'avg_review']])
        # replace average review with value one point lower if num_review is 0
        avg_num_reviews[avg_num_reviews[:, 0] == 0, 1] = avg_num_reviews[
            avg_num_reviews[:, 0] == 0, 1] - 1
        # fit and then normalise values, and then * 100 to get score
        n_average_rev = self.min_max_scaler.fit_transform(
            np.array(avg_num_reviews[:, 1]).reshape(
                (len(avg_num_reviews[:, 1]),
                 1)))*100
        print(np.ndim(n_average_rev))
        return(n_average_rev)

    # NUMBER OF PREVIOUS CLIENTS
    # Scored out of 50, as carers may have had previous clients before joining
    # But is still important if the brand requires certain traits in cariers,
    # And is also more reliable than years experience
    def calc_num_prev_clients(self):
        # extract no previous clients column
        num_prev_clients = np.array(self.carer_data['num_previous_clients']).reshape(
            (len(self.carer_data['num_previous_clients']), 1))
        # fit and normalise values, and then multiply by 50
        n_num_previous_cli = self.min_max_scaler.fit_transform(num_prev_clients) * 50
        print(np.ndim(n_num_previous_cli))
        return(n_num_previous_cli)

    # DAYS SINCE LAST LOGON
    # Score is out of 25
    # Data is modifies according to the number of previous clients to create
    # a greater disparity between those who have logged in a while ago
    # due to having current clients,
    # and those who have had no clients and have likely not logged in since signing up
    def calc_days_since_logon(self):
        # extract days since logon column
        days_since_log = np.array(self.carer_data['days_since_login'])
        # Get average and upper percentile logon times
        mean_login = np.mean(days_since_log)
        three_quart_percentile = np.percentile(days_since_log, 75)
        days_prev_clients = np.array(self.carer_data[['num_previous_clients', 'days_since_login']])
        # If no of previous clients is 0 and logon time is above agerage, double the days since logon
        days_prev_clients[np.logical_and(days_prev_clients[:, 0] == 0,
                          days_prev_clients[:, 1] > mean_login,
                          days_prev_clients[:, 1] <= three_quart_percentile), 1] = days_prev_clients[
                               np.logical_and(
                                   days_prev_clients[:, 0] == 0,
                                   days_prev_clients[:, 1] > mean_login,
                                   days_prev_clients[:, 1] <= three_quart_percentile
                               ),
                               1] * 2
        # If no of previous clients is 0 and logon time is above 75%, quadruple the days since logon
        days_prev_clients[np.logical_and(days_prev_clients[:, 0] == 0, 
                          days_prev_clients[:, 1] > three_quart_percentile), 1] = days_prev_clients[
                              np.logical_and(
                                  days_prev_clients[:, 0] == 0,
                                  days_prev_clients[:, 1] > three_quart_percentile
                              ), 1] * 4
        n_days_since_log = (1 - self.min_max_scaler.fit_transform(
                          days_prev_clients[:, 1].reshape(len(days_prev_clients[:, 1]), 1)
                          )) * 25
        print(np.ndim(n_days_since_log))
        return(n_days_since_log)

    # IMAGE PROBLEMS
    # Score is out of 25
    def calc_image_problems(self):
        img_problems = num_prev_clients = np.array(
            self.carer_data['img_problems']).reshape(
                (len(self.carer_data['img_problems']), 1))
        n_image_probs = (1 - self.min_max_scaler.fit_transform(img_problems)) * 25
        print(np.ndim(n_image_probs))
        return n_image_probs

    # Combine to make a big scoreboard and sort by best score
    def calc_final_score(self, years, review, clients, days, image):
        print(np.ndim(np.array(self.carer_data[['id', 'first_name',
                                       'last_name', 'num_reviews',
                                       'avg_review', 'img_problems', 'type',
                                       'num_previous_clients',
                                       'days_since_login', 'age',
                                       'years_experience']])))
        score_board = np.c_[np.array(self.carer_data[['id', 'first_name',
                                       'last_name', 'num_reviews',
                                       'avg_review', 'img_problems', 'type',
                                       'num_previous_clients',
                                       'days_since_login', 'age',
                                       'years_experience']]), years]
        """score_board = np.hstack(
            (np.array(self.carer_data[['id', 'first_name',
                                       'last_name', 'num_reviews',
                                       'avg_review', 'img_problems', 'type',
                                       'num_previous_clients',
                                       'days_since_login', 'age',
                                       'years_experience']]),
             years, review, clients, days, image))"""

        # From this, calculate the total score and sort by score
        sum_scores = score_board[:, 11] + score_board[:, 12] + score_board[:, 13] + score_board[:, 14] + score_board[:, 15]
        # append the total on the end of the scoreboard (for checking reasons)
        score_board = np.c_[score_board, sum_scores]
        # sort the carers by total score
        sorted_scores = score_board[np.argsort(sum_scores)][::-1]
        sorted_scores = np.vstack((['id', 'first_name', 'last_name', 'num_reviews',
                                    'avg_review', 'img_problems', 'type', 'num_previous_clients', 'days_since_login', 
                                    'age', 'years_experience', "total_score"],
                                  sorted_scores[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16]]))
        print("\n\n\n FINAL SORTED SCORES")
        print(sorted_scores)
        # save final scores in file
        np.savetxt("Best_carers_scoresheet.csv",
                   sorted_scores,
                   delimiter=",",
                   fmt="%s")


if __name__ == "__main__":
    carer_scorer = CarerScorer()
    carer_scorer.calc_years_experience()
    carer_scorer.calc_average_review()
    carer_scorer.calc_num_prev_clients()
    carer_scorer.calc_days_since_logon()
    carer_scorer.calc_image_problems()
    carer_scorer.calc_final_score(carer_scorer.calc_years_experience,
                                  carer_scorer.calc_average_review,
                                  carer_scorer.calc_num_prev_clients,
                                  carer_scorer.calc_days_since_logon,
                                  carer_scorer.calc_image_problems)
