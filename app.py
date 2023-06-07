
from flask import Flask, request, render_template, send_file
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)



class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(50))
    description = db.Column(db.String(200))
    imdb_rating = db.Column(db.Float)
    director = db.Column(db.String)
    genre = db.Column(db.String)
    year = db.Column(db.Integer)


    def to_dict(self):

        return {
            'id': self.id,
            'titel': self.titel,
            'description': self.description,
            'imdb_rating': self.imdb_rating,
            'director': self.director.split(','),
            'genre': self.genre.split(','),
            'year': self.year
        }
class Genres(db.Model):

    __tablename__ = 'genres'
    g_id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(255), unique=True)

    def to_dict(self):
        return {
            'g_id': self.g_id,
            'genre': self.genre
        }


class Directors(db.Model):
    __tablename__ = 'director'
    d_id = db.Column(db.Integer, primary_key=True)
    d_name = db.Column(db.String(255))
    d_lname = db.Column(db.String(255))

    def to_dict(self):
        return {
            'd_id': self.d_id,
            'd_name': self.d_name,
            'd_lname': self.d_lname
        }




# API Section for developers to use
# these use /api as main route
@app.route('/api/movies')
def get_movies():
    movies = [movie.to_dict() for movie in Movies.query.all()]
    return movies, 200

@app.route('/api/movies/<int:id>')
def get_movie_by_id(id):
    movie = Movies.query.get(id)
    return movie.to_dict(), 200


@app.route('/api/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    titel = data['titel']
    description = data['description']
    imdb_rating = data['imdb_rating']
    director = ','.join(str(x) for x in sorted(data['director']))
    genre = ','.join(str(x) for x in sorted(data['genre']))
    year = data['year']
    movie = Movies(titel=titel, description=description, imdb_rating=imdb_rating, director=director, genre=genre, year=year)
    db.session.add(movie)
    db.session.commit()
    return "Movie has been Added", 201


@app.route('/api/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    data = request.get_json()
    titel = data['titel']
    description = data['description']
    imdb_rating = data['imdb_rating']
    director = ','.join(str(x) for x in sorted(data['director']))
    genre = ','.join(str(x) for x in sorted(data['genre']))
    year = data['year']
    movie = Movies.query.get(id)
    if movie is not None:
        movie.titel = titel
        movie.description = description
        movie.imdb_rating = imdb_rating
        movie.director = director
        movie.genre = genre
        movie.year = year
        db.session.commit()
    return "Movie Has Been Updated", 200


@app.route('/api/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movies.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return "Movie has been Deleted", 200

@app.route('/api/genres')
def get_genres():
    genres = [genre.to_dict() for genre in Genres.query.all()]
    return genres, 200

@app.route('/api/genres/<int:id>')
def get_genre_by_id(id):
    genre = Genres.query.get(id)
    return genre.to_dict(), 200

@app.route('/api/genres', methods=['POST'])
def create_genre():
    data = request.get_json()
    genre = data['genre']
    payload = Movies(genre=genre)
    db.session.add(payload)
    db.session.commit()
    return "Genre has been Added", 201

@app.route('/api/genres/<int:id>', methods=['PUT'])
def update_genre(id):
    data = request.get_json()
    genre = data['genre']
    genre = Genres.query.get(id)
    if genre is not None:
        genre.genre = genre
        db.session.commit()
    return "Genre Has Been Updated", 200

@app.route('/api/genres/<int:id>', methods=['DELETE'])
def delete_genre(id):
    genre = Genres.query.get(id)
    db.session.delete(genre)
    db.session.commit()
    return "Genre has been Deleted", 200

@app.route('/api/directors')
def get_director():
    directors = [director.to_dict() for director in Directors.query.all()]
    return directors, 200

@app.route('/api/directors/<int:id>')
def get_directors_by_id(id):
    director = Directors.query.get(id)
    return director.to_dict(), 200

@app.route('/api/directors', methods=['POST'])
def create_director():
    data = request.get_json()
    d_name = data['d_name']
    d_lname = data['d_lname']
    payload = Movies(d_name=d_name, d_lname=d_lname)
    db.session.add(payload)
    db.session.commit()
    return "Director has been Added", 201

@app.route('/api/directors/<int:id>', methods=['PUT'])
def update_director(id):
    data = request.get_json()
    d_name = data['d_name']
    d_lname = data['d_lname']
    director = Directors.query.get(id)
    if director is not None:
        director.d_name = d_name
        director.d_lname = d_lname
        db.session.commit()
    return "director Has Been Updated", 200

@app.route('/api/directors/<int:id>', methods=['DELETE'])
def delete_director(id):
    director = Directors.query.get(id)
    db.session.delete(director)
    db.session.commit()
    return "director has been Deleted", 200



# Display Section of site, where html is being used
@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/')
def index_page():
    genres = [genre.to_dict() for genre in Genres.query.all()]
    movies = [movie.to_dict() for movie in Movies.query.all()]
    return render_template('index.html', movies=movies, genres=genres)


with app.app_context():
    db.create_all()
    app.run()