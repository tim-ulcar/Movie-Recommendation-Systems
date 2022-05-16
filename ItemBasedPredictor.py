from math import sqrt


class ItemBasedPredictor:
    def __init__(self, min_values=0, threshold=0):
        self.min_values = min_values
        self.threshold = threshold

    def fit(self, uid):
        self.uid = uid

        all_movieIDs_set = set()
        all_userIDs_set = set()
        userID_movieID_rating_dict = {}
        for userID, movieID, rating in zip(uid.userIDs, uid.movieIDs, uid.ratings):
            if userID not in userID_movieID_rating_dict:
                userID_movieID_rating_dict[userID] = {}
            userID_movieID_rating_dict[userID][movieID] = rating
            all_movieIDs_set.add(movieID)
            all_userIDs_set.add(userID)
        self.userID_movieID_rating_dict = userID_movieID_rating_dict
        self.all_movieIDs_set = all_movieIDs_set
        self.all_userIDs_set = all_userIDs_set

        average_ratings_dict = {}
        for userID, movieID_rating_dict in self.userID_movieID_rating_dict.items():
            users_ratings = []
            for movieID, rating in movieID_rating_dict.items():
                users_ratings.append(rating)
            average_ratings_dict[userID] = sum(users_ratings) / len(users_ratings)
        self.average_ratings_dict = average_ratings_dict

        #calculating all predicitons for all users
        # userID_movieID_prediction_dict = {}
        # for userID, movieID_rating_dict in self.userID_movieID_rating_dict.items():
        #     userID_movieID_prediction_dict[userID] = {}
        #     for movieID in all_movieIDs_set:
        #         if movieID in movieID_rating_dict:
        #             userID_movieID_prediction_dict[userID][movieID] = self.userID_movieID_rating_dict[userID][movieID]
        #         else:
        #             userID_movieID_prediction_dict[userID][movieID] = self.predicted_rating(userID, movieID)
        #         print("Prediction (userID, movieID, rating): ", userID, movieID, userID_movieID_prediction_dict[userID][movieID])
        # self.userID_movieID_prediction_dict = userID_movieID_prediction_dict

    def predicted_rating(self, userID, movieID_for_prediction):
        predictions_sum = 0
        weights_sum = 0
        for movieID, rating in self.userID_movieID_rating_dict[userID].items():
            weight = self.similarity(movieID, movieID_for_prediction)
            weights_sum += weight
            weighed_rating = weight * rating
            predictions_sum += weighed_rating
        if weights_sum == 0:
            prediction = 0
        else:
            prediction = predictions_sum / weights_sum
        return prediction

    def similarity(self, p1, p2):
        covariance = 0
        variance1 = 0
        variance2 = 0
        number_of_ratings = 0

        for userID, movieID_rating_dict in self.userID_movieID_rating_dict.items():
            if p1 in movieID_rating_dict and p2 in movieID_rating_dict:
                number_of_ratings += 1
                rating1 = movieID_rating_dict[p1]
                rating2 = movieID_rating_dict[p2]
                average_rating = self.average_ratings_dict[userID]
                covariance += (movieID_rating_dict[p1] - self.average_ratings_dict[userID]) * (movieID_rating_dict[p2] - self.average_ratings_dict[userID])
                variance1 += (movieID_rating_dict[p1] - self.average_ratings_dict[userID]) ** 2
                variance2 += (movieID_rating_dict[p2] - self.average_ratings_dict[userID]) ** 2
        if variance1 == 0 or variance2 == 0:
            print("Varaince is zero", userID)


        if not (variance1 == 0 or variance2 == 0):
            similarity = covariance / (sqrt(variance1) * sqrt(variance2))
            if similarity < self.threshold or number_of_ratings < self.min_values:
                similarity = 0
        else:
            similarity = 0

        return similarity

    def predict(self, userID):
        #if had already calculated all prediction for all users just use line below
        #return self.userID_movieID_prediction_dict[userID]

        movieID_prediction_dict = {}
        for movieID in self.all_movieIDs_set:
            if movieID in self.userID_movieID_rating_dict[userID]:
                movieID_prediction_dict[movieID] = self.userID_movieID_rating_dict[userID][movieID]
            else:
                movieID_prediction_dict[movieID] = self.predicted_rating(userID, movieID)
        return movieID_prediction_dict

    def similarItems(self, item, n):
        movieID_similarity = []
        for movieID in self.all_movieIDs_set:
            if movieID != item:
                movieID_similarity.append((movieID, self.similarity(item, movieID)))
        movieID_similarity = sorted(movieID_similarity, key=lambda tuple: tuple[1], reverse=True)
        return movieID_similarity[:n]

    def predict_for_all_users(self):
        userID_movieID_prediction_dict = {}
        for userID, movieID_rating_dict in self.userID_movieID_rating_dict.items():
            userID_movieID_prediction_dict[userID] = {}
            for movieID in self.all_movieIDs_set:
                if movieID in movieID_rating_dict:
                    userID_movieID_prediction_dict[userID][movieID] = self.userID_movieID_rating_dict[userID][movieID]
                else:
                    userID_movieID_prediction_dict[userID][movieID] = self.predicted_rating(userID, movieID)

        self.userID_movieID_prediction_dict = userID_movieID_prediction_dict
        return self.userID_movieID_prediction_dict
