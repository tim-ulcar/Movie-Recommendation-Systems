from math import sqrt
from UserItemData import pickle_save, pickle_load, UserItemData
from MovieData import MovieData
from RandomPredictor import RandomPredictor
from AveragePredictor import AveragePredictor
from ViewsPredictor import ViewsPredictor
from ItemBasedPredictor import ItemBasedPredictor
from SlopeOnePredictor import SlopeOnePredictor
from Recommender import Recommender

#Branje ocen
# uid = UserItemData('data/user_ratedmovies.dat')
# print(uid.nratings())
# pickle_save(uid, "uid_pickle.pickle")
uid = pickle_load("uid_pickle.pickle")
print("Branje ocen, število ocen (vsi podatki): ", uid.nratings())

# uid = UserItemData('data/user_ratedmovies.dat', from_date='12.1.2007', to_date='16.2.2008', min_ratings=100)
# print(uid.nratings())
# pickle_save(uid, "uid_min_ratings.pickle")
print("Branje ocen")
uid = pickle_load("uid_min_ratings.pickle")
print("Branje ocen, število ocen (omejeni podatki): ", uid.nratings())


#Branje filmov
#md = MovieData('data/movies.dat')
#print(md.get_title(1))
#pickle_save(md, "movie_data.pickle")
print()
print("Branje filmov")
md = pickle_load("movie_data.pickle")
print("Film z id 1: ", md.get_title(1))


#Naključni prediktor
print()
print("Naključni prediktor")
uid = pickle_load("uid_pickle.pickle")
md = pickle_load("movie_data.pickle")
rp = RandomPredictor(1, 5)
rp.fit(uid)
predictions = rp.predict(78)
print(type(predictions))
movieIDs = [1, 3, 20, 50, 100]
for movieID in movieIDs:
    print("Film: {}, ocena: {}".format(md.get_title(movieID), predictions[movieID]))


#Priporočanje
print()
print("Priporočanje")
print("RandomPredictor")
predictor = RandomPredictor(1, 5)
rec = Recommender(predictor)
rec.fit(uid)
rec_items = rec.recommend(78, n=5, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

print("AveragePredictor")
predictor = AveragePredictor(b=100)
rec = Recommender(predictor)
rec.fit(uid)
rec_items = rec.recommend(78, n=5, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

print("ViewsPredictor")
predictor = ViewsPredictor()
rec = Recommender(predictor)
rec.fit(uid)
rec_items = rec.recommend(78, n=5, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))


#Napovedovanje ocen s podobnostjo med produkti
print()
print("Napovedovanje ocen s podobnostjo med produkti")
uid = pickle_load('uid_min_1000.pickle')
predictor = ItemBasedPredictor()
rec = Recommender(predictor)
rec.fit(uid)
print("Podobnost med filmoma 'Men in black'(1580) in 'Ghostbusters'(2716): ", predictor.similarity(1580, 2716))
print("Podobnost med filmoma 'Men in black'(1580) in 'Schindler's List'(527): ", predictor.similarity(1580, 527))
print("Podobnost med filmoma 'Men in black'(1580) in 'Independence day'(780): ", predictor.similarity(1580, 780))
print("Predictions for 78: ")
rec_items = rec.recommend(78, n=15, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))


#Najbolj podobni filmi
print()
print("Najbolj podobni filmi")
movie1_movie2_similarity = []
for movie1 in rec.predictor.all_movieIDs_set:
    for movie2 in rec.predictor.all_movieIDs_set:
        if movie1 != movie2:
            movie1_movie2_similarity.append((movie1, movie2, rec.predictor.similarity(movie1, movie2)))
movie1_movie2_similarity = sorted(movie1_movie2_similarity, key=lambda tuple: tuple[2], reverse=True)
i = 20
for movie1, movie2, similarity in movie1_movie2_similarity:
    print("Film1: ", md.get_title(movie1), "Film2: ", md.get_title(movie2), "podobnost: ", similarity)
    i -= 1
    if i == 0:
        break

#Priporočanje glede na trenutno ogledano vsebino
print()
print("Priporočanje glede na trenutno ogledano vsebino")
rec_items = predictor.similarItems(4993, 10)
print('Filmi podobni "The Lord of the Rings: The Fellowship of the Ring": ')
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

#Priporočilo zase
print()
print("Priporočilo zase")
uid = pickle_load('uid_extended_min_1000.pickle')
predictor = ItemBasedPredictor()
rec = Recommender(predictor)
rec.fit(uid)
rec_items = rec.recommend(666666, n=10, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

#Napovedovanje z metodo Slope one
print()
print("Napovedovanje z metodo Slope one")
uid = pickle_load('uid_min_1000.pickle')
predictor = SlopeOnePredictor()
rec = Recommender(predictor)
rec.fit(uid)
print("Predictions for 78: ")
rec_items = rec.recommend(78, n=15, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

#Metoda evaluate
print()
print("Metoda evaluate")
uid = pickle_load('uid_min_1000_to_date_1-1-2008.pickle')
uid_test = pickle_load("uid_min_200_from_date_2-1-2008.pickle")
predictor = SlopeOnePredictor()
rec = Recommender(predictor)
rec.fit(uid)
rmse, mae, precision, recall, f = rec.evaluate(uid_test, 20)
print("SlopeOnePredictor - RMSE: ", rmse, " MAE: ", mae, " Precision: ", precision, " Recall: ", recall, " F: ", f)

predictor = ItemBasedPredictor()
rec = Recommender(predictor)
rec.fit(uid)
rmse, mae, precision, recall, f = rec.evaluate(uid_test, 20)
print("ItemBasedPredictor - RMSE: ", rmse, " MAE: ", mae, " Precision: ", precision, " Recall: ", recall, " F: ", f)
