import os, re, urllib, json
import tmdbsimple as tmdb

tmdb.API_KEY = "6a4bc831d3389b694627785af6f5320e"


class Movie:
    failed = False
    search = tmdb.Search()
    name = None
    year = None
    abspath = None
    director = None
    id = None
    poster_path = None

    # just pass file address as movie_file
    def __init__(self, movie_file=None, separator="-"):
        self.separator = separator
        if movie_file is not None:
            if os.path.isfile(movie_file):
            # try:
                self.init_name(movie_file)
                self.find_director()
            # except:
            #     self.failed = True

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

