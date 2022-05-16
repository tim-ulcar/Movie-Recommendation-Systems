class ViewsPredictor:
    def fit(self, uid):
        self.uid = uid

        movieID_n_ratings_dict = {}
        for movieID in uid.movieIDs:
            if movieID not in movieID_n_ratings_dict:
                movieID_n_ratings_dict[movieID] = 1
            else:
                movieID_n_ratings_dict[movieID] += 1

        self.movieID_n_ratings_dict = movieID_n_ratings_dict

    def predict(self, userID):
        return self.movieID_n_ratings_dict
