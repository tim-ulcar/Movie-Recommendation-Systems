from csv import DictReader
import pickle
import datetime


class UserItemData:
    def __init__(self, path, from_date=None, to_date=None, min_ratings=None):
        self.path = path
        self.from_date = from_date
        self.to_date = to_date
        self.min_ratings = min_ratings

        self.userIDs = []
        self.movieIDs = []
        self.ratings = []
        self.date_days = []
        self.date_months = []
        self.date_years = []
        self.date_hours = []
        self.date_minutes = []
        self.date_seconds = []

        movieID_nratings_dict = {}

        if from_date is not None or to_date is not None:
            if from_date is not None:
                from_date = datetime.datetime.strptime(from_date, "%d.%m.%Y")
            if to_date is not None:
                to_date = datetime.datetime.strptime(to_date, "%d.%m.%Y")
            with open(path, 'rt', encoding='utf-8') as file:
                reader = DictReader(file, delimiter='\t')
                for row in reader:
                    date = datetime.datetime(int(row["date_year"]), int(row["date_month"]), int(row["date_day"]))
                    if from_date is not None and to_date is not None:
                        if from_date <= date < to_date:
                            self.userIDs.append(int(row["userID"]))
                            self.movieIDs.append(int(row["movieID"]))
                            self.ratings.append(float(row["rating"]))
                            self.date_days.append(int(row["date_day"]))
                            self.date_months.append(int(row["date_month"]))
                            self.date_years.append(int(row["date_year"]))
                            self.date_hours.append(int(row["date_hour"]))
                            self.date_minutes.append(int(row["date_minute"]))
                            self.date_seconds.append(int(row["date_second"]))

                            movieID = int(row["movieID"])
                            if movieID in movieID_nratings_dict:
                                movieID_nratings_dict[movieID] += 1
                            else:
                                movieID_nratings_dict[movieID] = 1
                    elif from_date is not None and to_date is None:
                        if from_date <= date:
                            self.userIDs.append(int(row["userID"]))
                            self.movieIDs.append(int(row["movieID"]))
                            self.ratings.append(float(row["rating"]))
                            self.date_days.append(int(row["date_day"]))
                            self.date_months.append(int(row["date_month"]))
                            self.date_years.append(int(row["date_year"]))
                            self.date_hours.append(int(row["date_hour"]))
                            self.date_minutes.append(int(row["date_minute"]))
                            self.date_seconds.append(int(row["date_second"]))

                            movieID = int(row["movieID"])
                            if movieID in movieID_nratings_dict:
                                movieID_nratings_dict[movieID] += 1
                            else:
                                movieID_nratings_dict[movieID] = 1
                    elif from_date is None and to_date is not None:
                        if date < to_date:
                            self.userIDs.append(int(row["userID"]))
                            self.movieIDs.append(int(row["movieID"]))
                            self.ratings.append(float(row["rating"]))
                            self.date_days.append(int(row["date_day"]))
                            self.date_months.append(int(row["date_month"]))
                            self.date_years.append(int(row["date_year"]))
                            self.date_hours.append(int(row["date_hour"]))
                            self.date_minutes.append(int(row["date_minute"]))
                            self.date_seconds.append(int(row["date_second"]))

                            movieID = int(row["movieID"])
                            if movieID in movieID_nratings_dict:
                                movieID_nratings_dict[movieID] += 1
                            else:
                                movieID_nratings_dict[movieID] = 1

        else:
            with open(path, 'rt', encoding='utf-8') as file:
                reader = DictReader(file, delimiter='\t')
                for row in reader:
                    self.userIDs.append(int(row["userID"]))
                    self.movieIDs.append(int(row["movieID"]))
                    self.ratings.append(float(row["rating"]))
                    self.date_days.append(int(row["date_day"]))
                    self.date_months.append(int(row["date_month"]))
                    self.date_years.append(int(row["date_year"]))
                    self.date_hours.append(int(row["date_hour"]))
                    self.date_minutes.append(int(row["date_minute"]))
                    self.date_seconds.append(int(row["date_second"]))

                    movieID = int(row["movieID"])
                    if movieID in movieID_nratings_dict:
                        movieID_nratings_dict[movieID] += 1
                    else:
                        movieID_nratings_dict[movieID] = 1
        self.movieID_nratings_dict = movieID_nratings_dict

        if self.min_ratings is not None:
            movieIDs_to_remove = []
            for movieID, nratings in movieID_nratings_dict.items():
                if nratings < self.min_ratings:
                    movieIDs_to_remove.append(movieID)

            indexes_to_remove = []
            for index, movieID in enumerate(self.movieIDs):
                if movieID in movieIDs_to_remove:
                    indexes_to_remove.append(index)
                    print("Adding index to remove: ", index)

            indexes_to_remove = sorted(indexes_to_remove, reverse=True)
            for index in indexes_to_remove:
                self.userIDs.pop(index)
                self.movieIDs.pop(index)
                self.ratings.pop(index)
                self.date_days.pop(index)
                self.date_months.pop(index)
                self.date_years.pop(index)
                self.date_hours.pop(index)
                self.date_minutes.pop(index)
                self.date_seconds.pop(index)

    def nratings(self):
        return len(self.userIDs)


def pickle_save(something, fileName):
    with open(fileName, 'wb') as file:
        pickle.dump(something, file)


def pickle_load(fileName):
    with open(fileName, 'rb') as file:
        something = pickle.load(file)
        return something

def delete_multiple_elements(list, indices):
    indices = sorted(indices, reverse=True)
    for index in indices:
        list.pop(index)


# uid = UserItemData('data/user_ratedmovies.dat')
# print(uid.nratings())
# pickle_save(uid, "uid_pickle.pickle")

# uid = pickle_load("uid_pickle.pickle")
# print(uid.nratings())

# uid = UserItemData('data/user_ratedmovies.dat', from_date='12.1.2007', to_date='16.2.2008', min_ratings=100)
# print(uid.nratings())
# pickle_save(uid, "uid_min_ratings.pickle")
