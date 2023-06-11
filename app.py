
from Database import MoviesDatabase
from Database import DirectorDatabase
from Database import GenreDatabase
from Database import MovieGenreConnect
from Database import MovieDirectorConnect
from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = '/movies.db'
moviesdb = MoviesDatabase()
genredb = GenreDatabase()
directordb = DirectorDatabase()
moviegenre = MovieGenreConnect()
moviedirector = MovieDirectorConnect()

# API Section for developers to use
# these use /api as main route
@app.route('/api/movies')
def get_movies():
    movies = moviesdb.get_all_movies()
    print(movies)
    return movies, 200


@app.route('/api/movies/<int:id>')
def get_movie_by_id(id):
    movie = moviesdb.get_movie_by_id(id)
    return movie, 200


@app.route('/api/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    title = data['title']
    description = data['description']
    imdb_rating = data['imdb_rating']
    year = data['year']
    moviesdb.add_movie(title, description, imdb_rating, year)
    return "Movie has been Added", 201


@app.route('/api/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    data = request.get_json()
    title = data['title']
    description = data['description']
    imdb_rating = data['imdb_rating']
    year = data['year']
    moviesdb.update_movie(id, title, description, imdb_rating, year)
    return "Movie Has Been Updated", 200


@app.route('/api/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    moviesdb.delete_movie(id)
    return "Movie has been Deleted", 200


@app.route('/api/genres')
def get_genres():
    genres = genredb.get_all_genres()
    return genres, 200


@app.route('/api/genres/<int:id>')
def get_genre_by_id(id):
    genre = genredb.get_genre_by_id(id)
    return genre.to_dict(), 200


@app.route('/api/genres', methods=['POST'])
def create_genre():
    data = request.get_json()
    genre = data['genre']
    genredb.add_genre(genre)
    return "Genre has been Added", 201


@app.route('/api/genres/<int:id>', methods=['PUT'])
def update_genre(id):
    data = request.get_json()
    genre = data['genre']
    genredb.update_genre(id, genre)
    return "Genre Has Been Updated", 200


@app.route('/api/genres/<int:id>', methods=['DELETE'])
def delete_genre(id):
    genredb.delete_genre(id)
    return "Genre has been Deleted", 200


@app.route('/api/directors')
def get_director():
    directors = directordb.get_all_directors()
    return directors, 200


@app.route('/api/directors/<int:id>')
def get_directors_by_id(id):
    director = directordb.get_director_by_id(id)
    return director, 200


@app.route('/api/directors', methods=['POST'])
def create_director():
    data = request.get_json()
    d_name = data['d_name']
    d_lname = data['d_lname']
    directordb.add_director(d_name, d_lname)
    return "Director has been Added", 201


@app.route('/api/directors/<int:id>', methods=['PUT'])
def update_director(id):
    data = request.get_json()
    d_name = data['d_name']
    d_lname = data['d_lname']
    directordb.update_director(id, d_name, d_lname)
    return "director Has Been Updated", 200


@app.route('/api/directors/<int:id>', methods=['DELETE'])
def delete_director(id):
    directordb.delete_director(id)
    return "director has been Deleted", 200


# Display Section of site, where html is being used
@app.route('/upload')
def upload_page():
    directors = directordb.get_directors_order_by_lname()
    genres = genredb.get_genres_by_alphabet()
    return render_template('upload.html', directors=directors, genres=genres)


@app.route('/')
def index():
    movies = moviesdb.get_all_movies()
    return render_template('index.html', movies=movies)

@app.route('/search')
def search_results():
    query = request.args.get('query')
    movies = moviesdb.search_movies_by_title(f'%{query}%')
    return render_template('search_results.html', movies=movies)


@app.route('/api/movies/top_10')
def get_top():
    movies = moviesdb.get_top10()
    return movies


@app.route('/movies/<int:idnum>', methods=['POST', 'GET'])
def movie_info(idnum):
    movie = moviesdb.get_movie_by_id(idnum)

    # Now we Search for Directors
    participated_directors = moviedirector.get_directos_by_movie(idnum)
    # All used genres used in Movie
    used_genres = moviegenre.get_genres_by_movie(idnum)

    recommended_movies = []
    for direcotor in participated_directors:
        d_movies = moviedirector.get_movies_by_by(direcotor["d_id"])
        recommended_movies.append({'d_id': direcotor["d_id"], 'd_fullname': direcotor['d_fullname'], 'movies': d_movies})
    print(recommended_movies)


    if movie is None:
        return "No Page Found"
    else:
        return render_template('movie_display.html', movie=movie, participated_directors=participated_directors, used_genres=used_genres, recommended_movies=recommended_movies)

with app.app_context():
    app.run()
