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

# curl -X POST -H "Content-Type: application/json" -d '{"title": "Kai KAaci", "description": "ra ubedurbeaaa", "imdb_rating": 6.9, "directors": ["Maisa Best", 1, 5, "Mamida Manqanit"], "genres": [1, 5, 2, 7, 4], "year": 2001}' http://127.0.0.1:5000/api/movies

moviesdb.get_all_movies_across_tables()