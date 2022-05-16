from UserItemData import UserItemData
from MovieData import MovieData
import random
import pickle


class RandomPredictor:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def fit(self, uid):
        self.uid = uid

    def predict(self, userID):
        predictions_dict = {}
        for movieID in self.uid.movieIDs:
            predictions_dict[movieID] = random.randint(self.min, self.max)
        return predictions_dict


def pickle_save(something, fileName):
    with open(fileName, 'wb') as file:
        pickle.dump(something, file)


def pickle_load(fileName):
    with open(fileName, 'rb') as file:
        something = pickle.load(file)
        return something

"""
uid = pickle_load("uid_pickle.pickle")
# uid = UserItemData('data/user_ratedmovies.dat')
# pickle_save(uid, "uid_pickle.pickle")
md = pickle_load("movie_data.pickle")
rp = RandomPredictor(1, 5)
rp.fit(uid)
predictions = rp.predict(78)
print(type(predictions))
movieIDs = [1, 3, 20, 50, 100]
for movieID in movieIDs:
    print("Film: {}, ocena: {}".format(md.get_title(movieID), predictions[movieID]))
"""