import random
from Database import MoviesDatabase
from Database import DirectorDatabase
from Database import GenreDatabase
from Database import MovieGenreConnect
from Database import MovieDirectorConnect


moviesdb = MoviesDatabase()
genredb = GenreDatabase()
directordb = DirectorDatabase()
moviegenre = MovieGenreConnect()
moviedirector = MovieDirectorConnect()

print(moviedirector.get_movies_by_by(3))
for i in moviedirector.get_movies_by_by(3):
    print(i)
