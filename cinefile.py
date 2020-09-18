import os, re, urllib, json, shutil
import traceback

import tmdbsimple as tmdb
from PIL import Image

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
                except Exception as exc:
                    print traceback.format_exc()
                    print exc
                    self.failed = True

    def init_name(self, movie_file):
        newname = re.sub("[_.]", " ", os.path.basename(movie_file))
        findall = re.findall(r"\d{4}", newname)

        z = 0
        if int(findall[0]) > 2020:
            z = 1

        if findall[z] != "1080":
            self.year = int(findall[z])
            self.name = re.split(r"\d{4}", newname)[0].strip()
            self.abspath = os.path.abspath(movie_file).strip()

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
                self.director = personnel['name'].encode("utf-8").strip()
                break

    def __str__(self):
        return self.name + " " + str(self.year) + " : " + self.director


class Manager:  # pass working folder path
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

        for i in listd:
            try:
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
            except Exception as exc:
                print traceback.format_exc()
                print exc

    @staticmethod
    def generate_fname(movie):  # generates folder name TODO read from config how to do it
        return str(movie.year) + " - " + movie.name

    def make_folders(self):  # Should scan folder first, movie_list should not be empty
        work_folder = self.basefolder + os.path.sep + "CineFile"
        try:
            os.mkdir(work_folder)
        except Exception as exc:
            print traceback.format_exc()
            print exc
            self.status = "Problem working with folder"
            return

        for movie in self.movie_list:
            movie_dir = work_folder + os.path.sep + movie.director + os.path.sep + Manager.generate_fname(movie)

            try:
                if os.path.isdir(work_folder + os.path.sep + movie.director):
                    if not os.path.isdir(movie_dir):
                        os.mkdir(movie_dir)
                else:
                    os.mkdir(work_folder + os.path.sep + movie.director)
                    os.mkdir(movie_dir)

                if not os.path.isfile(movie_dir + os.path.sep + os.path.basename(movie.abspath)):
                    os.rename(movie.abspath, movie_dir + os.path.sep + os.path.basename(movie.abspath))

            except Exception as exc:
                print traceback.format_exc()
                print exc
                print(movie.abspath, movie_dir + os.path.sep + os.path.basename(movie.abspath))
                self.status = "Problem Writing the File"


class Icon:
    desktopini = '[.ShellClassInfo] \nIconResource=icon.ico,0 \n'

    def __init__(self):
        pass

    @staticmethod
    def expand2square(pil_img, background_color=0):  # copied this from note.nkmk.me
        width, height = pil_img.size
        if width == height:
            return pil_img
        elif width > height:
            result = Image.new(pil_img.mode, (width, width), background_color)
            result.paste(pil_img, (0, (width - height) // 2))
            return result
        else:
            result = Image.new(pil_img.mode, (height, height), background_color)
            result.paste(pil_img, ((height - width) // 2, 0))
            return result


class DirectorIcon:  # pass Directors folder, like CineFile folder
    status = ""
    total_progress = 0
    done_progress = 0
    director_icons = dict()  # { links folder path to jpg URL }

    def __init__(self, basefolder):
        self.basefolder = basefolder

    def scan_folder(self):  # check self.movie_list afterwards!
        # self.total_progress = MovieScanner.count_progress(self.basefolder) # TODO change this
        listd = os.listdir(self.basefolder)

        for item in listd:
            try:
                self.validate_director(item)
            except Exception as exc:
                print traceback.format_exc()
                print exc
                self.status = "Problem with API"

    def validate_director(self, name):
        if "desktop.ini" in os.listdir(self.basefolder + os.path.sep + name):
            return

        search = tmdb.Search()
        person = search.person(query=name)
        if person['total_results'] != 0:
            self.director_icons[self.basefolder + os.path.sep + name] = person['results'][0]['profile_path']
            self.status = "Recognized " + name

    def set_icons(self):  # should scan first, director_icons should not be empty
        for folderpath in self.director_icons:
            if self.director_icons[folderpath] is None:
                continue

            url = urllib.urlopen("https://image.tmdb.org/t/p/w200/" + self.director_icons[folderpath])
            im = Image.open(url).convert('RGBA')
            im_new = Icon.expand2square(im)
            im_new.convert("L")
            im_new.save(folderpath + os.path.sep + "icon.ico")
            os.system("attrib +H \""+ folderpath + os.path.sep + "icon.ico\"")

            self.set_icon(folderpath)

    def set_icon(self, folderpath):
        try:
            with open(folderpath + os.path.sep + "desktop.ini", "w") as f:
                f.write(Icon.desktopini)
                f.close()
        except Exception as exc:
            print traceback.format_exc()
            print exc
            self.status = "Problem in writing desktop.ini"

        try:
            os.system('attrib +S +H "'+ folderpath + os.path.sep + 'desktop.ini"')
            os.system('attrib +R "'+folderpath+'"')
        except Exception as exc:
            print traceback.format_exc()
            print exc
            self.status = "Problem with setting icon"


