from math import sqrt
from UserItemData import pickle_save, pickle_load, UserItemData
from RandomPredictor import RandomPredictor
from AveragePredictor import AveragePredictor
from ViewsPredictor import ViewsPredictor
from ItemBasedPredictor import ItemBasedPredictor
from SlopeOnePredictor import SlopeOnePredictor

class Recommender:
    def __init__(self, predictor):
        self.predictor = predictor

    def fit(self, uid):
        self.uid = uid
        self.predictor.fit(uid)

    def recommend(self, userID, n=10, rec_seen=True):
        predictions = self.predictor.predict(userID)
        recommendations = sorted(predictions.items(), key=lambda tuple: tuple[1], reverse=True)
        final_list = []
        for movieID, rating in recommendations:
            if len(final_list) >= n:
                return final_list
            else:
                if rec_seen:
                    final_list.append((movieID, rating))
                else:
                    if not self.has_seen_the_movie(userID, movieID):
                        final_list.append((movieID, rating))
        return final_list

    def has_seen_the_movie(self, user_tested, movie_tested):
        for i, userID in enumerate(self.uid.userIDs):
            if userID == user_tested:
                if movie_tested == self.uid.movieIDs[i]:
                    return True
        return False

    def evaluate(self, test_data, n):
        userID_movieID_prediction_dict = {}
        userID_recommendations_dict = {}
        for userID in test_data.userIDs:
            if userID not in userID_movieID_prediction_dict and userID in self.predictor.all_userIDs_set:
                movieID_prediction_dict = self.predictor.predict(userID)
                userID_movieID_prediction_dict[userID] = movieID_prediction_dict
                recommendations_tuples = self.recommend(userID, n=n, rec_seen=False)
                recommendations = []
                for id, rating in recommendations_tuples:
                    recommendations.append(id)
                userID_recommendations_dict[userID] = recommendations

        number_of_ratings = 0
        sum_mse = 0
        sum_mae = 0
        userID_relevant_matches_dict = {}
        userID_number_of_relevant_movies_dict = {}
        for userID, movieID, rating in zip(test_data.userIDs, test_data.movieIDs, test_data.ratings):
            if userID in self.predictor.all_userIDs_set and movieID in self.predictor.all_movieIDs_set:
                sum_mse += (userID_movieID_prediction_dict[userID][movieID] - rating) ** 2
                sum_mae += abs(userID_movieID_prediction_dict[userID][movieID] - rating)
                number_of_ratings += 1
                #if the movie is relevant
                if rating > self.predictor.average_ratings_dict[userID]:
                    if userID in userID_number_of_relevant_movies_dict:
                        userID_number_of_relevant_movies_dict[userID] += 1
                    else:
                        userID_number_of_relevant_movies_dict[userID] = 1
                    #if the the relevant movie was recommended
                    if movieID in userID_recommendations_dict[userID]:
                        if userID in userID_relevant_matches_dict:
                            userID_relevant_matches_dict[userID] += 1
                        else:
                            userID_relevant_matches_dict[userID] = 1

        mse = sum_mse / number_of_ratings
        rmse = sqrt(mse)
        mae = sum_mae / number_of_ratings

        precisions = []
        recalls = []
        for userID, relevant_matches in userID_relevant_matches_dict.items():
            precisions.append(relevant_matches / n)
            recalls.append(relevant_matches / userID_number_of_relevant_movies_dict[userID])
        precision = sum(precisions) / len(precisions)
        recall = sum(recalls) / len(recalls)
        f = (2 * precision * recall) / (precision + recall)

        return (rmse, mae, precision, recall, f)




#uim = pickle_load('uid_pickle.pickle')
#md = pickle_load('movie_data.pickle')
#predictor = RandomPredictor(1, 5)
#predictor = AveragePredictor(b=100)
"""
predictor = ViewsPredictor()
rec = Recommender(predictor)
rec.fit(uim)
rec_items = rec.recommend(78, n=5, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))
"""

# uid = UserItemData('data/user_ratedmovies.dat', min_ratings=1000)
# pickle_save(uid, "uid_min_1000.pickle")
# uid = pickle_load('uid_pickle.pickle')
#uid = pickle_load('uid_min_1000.pickle')
# uid = UserItemData('data/extended_user_ratedmovies.dat', min_ratings=1000)
# pickle_save(uid, "uid_extended_min_1000.pickle")
# uid = UserItemData('data/user_ratedmovies.dat', min_ratings=1000, to_date='1.1.2008')
# pickle_save(uid, "uid_min_1000_to_date_1-1-2008.pickle")
uid = pickle_load("uid_min_1000_to_date_1-1-2008.pickle")

md = pickle_load('movie_data.pickle')
predictor = SlopeOnePredictor()
rec = Recommender(predictor)
rec.fit(uid)
#pickle_save(rec, "rec_with_ibp.pickle")

# print("Podobnost med filmoma 'Men in black'(1580) in 'Ghostbusters'(2716): ", predictor.similarity(1580, 2716))
# print("Podobnost med filmoma 'Men in black'(1580) in 'Schindler's List'(527): ", predictor.similarity(1580, 527))
# print("Podobnost med filmoma 'Men in black'(1580) in 'Independence day'(780): ", predictor.similarity(1580, 780))
#
# print("Predictions for 78: ")
# rec_items = rec.recommend(78, n=15, rec_seen=False)
# for idmovie, val in rec_items:
#     print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))
#
# print("Most similar movies:")
# movie1_movie2_similarity = []
# for movie1 in rec.predictor.all_movieIDs_set:
#     for movie2 in rec.predictor.all_movieIDs_set:
#         if movie1 != movie2:
#             movie1_movie2_similarity.append((movie1, movie2, rec.predictor.similarity(movie1, movie2)))
# movie1_movie2_similarity = sorted(movie1_movie2_similarity, key=lambda tuple: tuple[2], reverse=True)
#
# i = 20
# for movie1, movie2, similarity in movie1_movie2_similarity:
#     print("Film1: ", md.get_title(movie1), "Film2: ", md.get_title(movie2), "podobnost: ", similarity)
#     i -= 1
#     if i == 0:
#         break

# rec_items = predictor.similarItems(4993, 10)
# print('Filmi podobni "The Lord of the Rings: The Fellowship of the Ring": ')
# for idmovie, val in rec_items:
#     print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

# print("Predictions for me: ")
# rec_items = rec.recommend(666666, n=10, rec_seen=False)
# for idmovie, val in rec_items:
#     print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

# uid_test = UserItemData('data/user_ratedmovies.dat', min_ratings=200, from_date='2.1.2008')
# pickle_save(uid_test, "uid_min_200_from_date_2-1-2008.pickle")

# uid_test = pickle_load("uid_min_200_from_date_2-1-2008.pickle")
# rmse, mae, precision, recall, f = rec.evaluate(uid_test, 20)
# print(rmse, mae, precision, recall, f)
