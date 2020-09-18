import os, re, urllib, json, shutil
import tmdbsimple as tmdb

tmdb.API_KEY = "6a4bc831d3389b694627785af6f5320e"


class Movie:      # just pass file address as input, failed will be True if some problem happens
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
        return  self.name + " " + str(self.year) + " : " + self.director


class Manager:
    status = ""  # Send Status For GUI
    total_progress = 0  # Progress Bar Data for GUI
    done_progress = 0
    movie_list = list()

    def __init__(self, basefolder):
        self.basefolder = basefolder

    @staticmethod
    def count_progress(folder):
        total_progress = 0
        for item in os.listdir(folder):
            total_progress += 1
            if os.path.isdir(folder + os.path.sep + item):
                total_progress += Manager.count_progress(folder + os.path.sep + item)
        return total_progress

    def scan_folder(self, folder=None):  # check self.movie_list afterwards!
        self.total_progress = Manager.count_progress(self.basefolder)
        folder = self.basefolder if folder is None else folder
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
                            print(self.status)
                            self.movie_list.append(movie)
                        else:
                            del movie
                self.done_progress += 1
        except:
            pass

    @staticmethod
    def generate_fname(movie): # generates folder name TODO read from config how to do it
        return str(movie.year) + " - " + movie.name

    def make_folders(self): # Should scan folder first, movie_list should not be empty
        work_folder = self.basefolder + os.path.sep + "CineFile"
        try:
            os.mkdir(work_folder)
        except:
            self.status = "Problem working with folder"
            return
        try:
            for movie in self.movie_list:
                movie_dir = work_folder + os.path.sep + movie.director + os.path.sep + Manager.generate_fname(movie)
                if os.path.isdir(work_folder + os.path.sep + movie.director):
                    if not os.path.isdir(movie_dir):
                        os.mkdir(movie_dir)
                else:
                    os.mkdir(work_folder + os.path.sep + movie.director)
                    os.mkdir(movie_dir)

                if not os.path.isfile(movie_dir + os.path.sep + os.path.basename(movie.abspath)):
                    os.rename(movie.abspath, movie_dir + os.path.sep + os.path.basename(movie.abspath))
        except:
            self.status = "Problem Writing the File"


class DirectorIcon: # pass Directors folder, like CineFile folder
    status = ""
    total_progress = 0
    done_progress = 0
    director_icons = dict() # { links folder path to icon URL }

    def __init__(self, basefolder):
        self.basefolder = basefolder

    def scan_folder(self):  # check self.movie_list afterwards!
        # self.total_progress = MovieScanner.count_progress(self.basefolder) # TODO change this
        listd = os.listdir(self.basefolder)

        for item in listd:
            try:
                self.validate_director(item)
            except:
                print("Problem with API")


    def validate_director(self, name):
        search = tmdb.Search()
        person = search.person(query=name)
        if person['total_results'] != 0:
            self.director_icons[name] = person['results'][0]['profile_path']