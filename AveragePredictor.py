class AveragePredictor:
    def __init__(self, b):
        self.b = b

    def fit(self, uid):
        self.uid = uid

        movieID_ratings_dict = {}
        all_ratings = []
        for movieID, rating in zip(uid.movieIDs, uid.ratings):
            all_ratings.append(rating)
            if movieID not in movieID_ratings_dict:
                movieID_ratings_dict[movieID] = [rating]
            else:
                movieID_ratings_dict[movieID].append(rating)

        average_rating = sum(all_ratings) / len(all_ratings)
        movieID_average_dict = {}
        for movieID, ratings in movieID_ratings_dict.items():
            movieID_average_dict[movieID] = (sum(ratings) + self.b * average_rating) / (len(ratings) + self.b)

        self.movieID_average_dict = movieID_average_dict

    def predict(self, userID):
        return self.movieID_average_dict

