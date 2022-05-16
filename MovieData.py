from csv import DictReader
import pickle


class MovieData:
    def __init__(self, path):
        self.path = path

        self.ids = []
        self.titles = []
        self.imdbIDs = []
        self.spanishTitles = []
        self.imdbPictureURLs = []
        self.years = []
        self.rtIDs = []
        self.rtAllCriticsRatings = []
        self.rtAllCriticsNumReviewss = []
        self.rtAllCriticsNumFreshs = []
        self.rtAllCriticsNumRottens = []
        self.rtAllCriticsScores = []
        self.rtTopCriticsRatings = []
        self.rtTopCriticsNumReviewss = []
        self.rtTopCriticsNumFreshs = []
        self.rtTopCriticsNumRottens = []
        self.rtTopCriticsScores = []
        self.rtAudienceRatings = []
        self.rtAudienceNumRatingss = []
        self.rtAudienceScores = []
        self.rtPictureURLs = []

        self.id_title_dict = {}
        with open(path, 'rt', encoding='ansi') as file:
            reader = DictReader(file, delimiter='\t')
            for row in reader:
                self.ids.append(int(row["id"]))
                self.titles.append(row["title"])
                self.imdbIDs.append(int(row["imdbID"]))
                self.spanishTitles.append(["spanishTitle"])
                self.imdbPictureURLs.append(["imdbPictureURL"])
                self.years.append(int(row["year"]))
                self.rtIDs.append(row["rtID"])

                if row["rtAllCriticsRating"] != '\\N':
                    self.rtAllCriticsRatings.append(float(row["rtAllCriticsRating"]))
                else:
                    self.rtAllCriticsRatings.append(row["rtAllCriticsRating"])

                if row["rtAllCriticsNumReviews"] != '\\N':
                    self.rtAllCriticsNumReviewss.append(int(row["rtAllCriticsNumReviews"]))
                else:
                    self.rtAllCriticsNumReviewss.append(row["rtAllCriticsNumReviews"])

                if row["rtAllCriticsNumFresh"] != '\\N':
                    self.rtAllCriticsNumFreshs.append(int(row["rtAllCriticsNumFresh"]))
                else:
                    self.rtAllCriticsNumFreshs.append(row["rtAllCriticsNumFresh"])

                if row["rtAllCriticsNumRotten"] != '\\N':
                    self.rtAllCriticsNumRottens.append(int(row["rtAllCriticsNumRotten"]))
                else:
                    self.rtAllCriticsNumRottens.append(row["rtAllCriticsNumRotten"])

                if row["rtAllCriticsScore"] != '\\N':
                    self.rtAllCriticsScores.append(int(row["rtAllCriticsScore"]))
                else:
                    self.rtAllCriticsScores.append(row["rtAllCriticsScore"])

                if row["rtTopCriticsRating"] != '\\N':
                    self.rtTopCriticsRatings.append(float(row["rtTopCriticsRating"]))
                else:
                    self.rtTopCriticsRatings.append(row["rtTopCriticsRating"])

                if row["rtTopCriticsNumReviews"] != '\\N':
                    self.rtTopCriticsNumReviewss.append(int(row["rtTopCriticsNumReviews"]))
                else:
                    self.rtTopCriticsNumReviewss.append(row["rtTopCriticsNumReviews"])

                if row["rtTopCriticsNumFresh"] != '\\N':
                    self.rtTopCriticsNumFreshs.append(int(row["rtTopCriticsNumFresh"]))
                else:
                    self.rtTopCriticsNumFreshs.append(row["rtTopCriticsNumFresh"])

                if row["rtTopCriticsNumRotten"] != '\\N':
                    self.rtTopCriticsNumRottens.append(int(row["rtTopCriticsNumRotten"]))
                else:
                    self.rtTopCriticsNumRottens.append(row["rtTopCriticsNumRotten"])

                if row["rtTopCriticsScore"] != '\\N':
                    self.rtTopCriticsScores.append(int(row["rtTopCriticsScore"]))
                else:
                    self.rtTopCriticsScores.append(row["rtTopCriticsScore"])

                if row["rtAudienceRating"] != '\\N':
                    self.rtAudienceRatings.append(float(row["rtAudienceRating"]))
                else:
                    self.rtAudienceRatings.append(row["rtAudienceRating"])

                if row["rtAudienceNumRatings"] != '\\N':
                    self.rtAudienceNumRatingss.append(int(row["rtAudienceNumRatings"]))
                else:
                    self.rtAudienceNumRatingss.append(row["rtAudienceNumRatings"])

                if row["rtAudienceScore"] != '\\N':
                    self.rtAudienceScores.append(int(row["rtAudienceScore"]))
                else:
                    self.rtAudienceScores.append(row["rtAudienceScore"])

                self.rtPictureURLs.append(row["rtPictureURL"])

                self.id_title_dict[int(row["id"])] = row["title"]

    def get_title(self, movieID):
        return self.id_title_dict[movieID]


def pickle_save(something, fileName):
    with open(fileName, 'wb') as file:
        pickle.dump(something, file)


def pickle_load(fileName):
    with open(fileName, 'rb') as file:
        something = pickle.load(file)
        return something


#md = MovieData('data/movies.dat')
#print(md.get_title(1))
#pickle_save(md, "movie_data.pickle")
# md = pickle_load("movie_data.pickle")
# print(md.get_title(1))
