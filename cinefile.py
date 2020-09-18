import os, re, urllib, json
import tmdbsimple as tmdb

tmdb.API_KEY = "6a4bc831d3389b694627785af6f5320e"


class Movie:  # just pass file address as input, failed will be True if some problem happens
    failed = False
    search = tmdb.Search()
    name = None
    year = None
    abspath = None
    director = None
    id = None
    poster_path = None

    def __init__(self, movie_file=None):
        if movie_file is not None:
            if os.path.isfile(movie_file):
                try:
                    self.init_name(movie_file)
                    self.find_director()
                    self.failed = True if self.name is None or self.year is None or self.id is None or self.director is None \
                        else False
                except:
                    self.failed = True

    def init_name(self, movie_file):
        newname = re.sub("[_.]", " ", os.path.basename(movie_file))
        findall = re.findall(r"\d{4}", newname)

        z = 0
        if int(findall[0]) > 2020:
            z = 1

        if findall[z] != "1080":
            self.year = int(findall[z])
            self.name = re.split(r"\d{4}", newname)[0]
            self.abspath = os.path.abspath(movie_file)

    def find_director(self):
        self.search.movie(query=self.name)

        for movie in self.search.results:
            result_year = int(re.split('-', movie['release_date'])[0])
            if abs(self.year - result_year) <= 1:
                self.id = int(movie['id'])
                self.poster_path = movie['poster_path']
                break

        movie = tmdb.Movies(self.id)
        for personnel in movie.credits()['crew']:
            if personnel['job'] == "Director":
                self.director = personnel['name']
                break

    def __str__(self):
        return str(self.year) + "," + self.name + "," + self.director


class Manager:
    status = ""  # Send Status For GUI
    total_progress = 0  # Progress Bar Data for GUI
    done_progress = 0
    movie_list = list()

    def __init__(self, basefolder, outfolder):
        self.outfolder = outfolder
        self.folder = basefolder
        self.total_progress = Manager.count_progress(basefolder)

    @staticmethod
    def count_progress(folder):
        total_progress = 0
        for item in os.listdir(folder):
            total_progress += 1
            if os.path.isdir(folder + os.path.sep + item):
                total_progress += Manager.count_progress(folder + os.path.sep + item)
        return total_progress

    def scan_folder(self, folder=None):  # check self.movie_list afterwards!
        folder = self.folder if folder is None else folder
        folder = folder + os.path.sep
        listd = os.listdir(folder)

        formats = ["mp4", "mkv", "avi", "flv", "avi", "wmv"]
        try:
            for i in listd:
                if os.path.isdir(folder + i):
                    self.scan_folder(folder + i + os.path.sep)
                else:
                    if i[-3:] in formats:
                        movie = Movie(folder + i)
                        if not movie.failed:
                            self.status = "Recognized " + str(movie)
                            self.movie_list.append(movie)
                        else:
                            del movie
        except:
            pass


m = Manager("/media/mehdi/Mehdi")
m.scan_folder()
print(str(m.movie_list))
