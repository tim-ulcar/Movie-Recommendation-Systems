class SlopeOnePredictor:
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

    def predicted_rating(self, userID, movieID_for_prediction):
        sum = 0
        number_of_ratings = 0

        for movieID, rating in self.userID_movieID_rating_dict[userID].items():
            dev, n = self.get_dev(movieID_for_prediction, movieID)
            number_of_ratings += n
            sum += (rating + dev) * n

        if number_of_ratings != 0:
            prediction = sum / number_of_ratings
        else:
            prediction = 0

        return prediction

    def get_dev(self, p1, p2):
        sum = 0
        number_of_ratings = 0

        for userID, movieID_rating_dict in self.userID_movieID_rating_dict.items():
            if p1 in movieID_rating_dict and p2 in movieID_rating_dict:
                number_of_ratings += 1
                sum += (movieID_rating_dict[p1] - movieID_rating_dict[p2])

        if (number_of_ratings != 0):
            dev = sum / number_of_ratings
        else:
            dev = 0
        return (dev, number_of_ratings)

    def predict(self, userID):
        movieID_prediction_dict = {}
        for movieID in self.all_movieIDs_set:
            if movieID in self.userID_movieID_rating_dict[userID]:
                movieID_prediction_dict[movieID] = self.userID_movieID_rating_dict[userID][movieID]
            else:
                movieID_prediction_dict[movieID] = self.predicted_rating(userID, movieID)
        return movieID_prediction_dict

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
