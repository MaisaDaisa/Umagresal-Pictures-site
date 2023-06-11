import sqlite3


class Director:
    def __init__(self, d_id, d_name, d_lname):
        self.d_id = d_id
        self.d_name = d_name
        self.d_lname = d_lname


class MoviesDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('movies.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY,
                title VARCHAR(50),
                description VARCHAR(200),
                imdb_rating FLOAT,
                year INTEGER
            );
        """)

    def add_movie(self, title, description, imdb_rating, year):
        last_id = self.get_last_id()+1
        self.cursor.execute("""
            INSERT INTO movies VALUES 
            (?, ?, ?, ?, ?)
        """, (last_id, title, description, imdb_rating, year))
        self.conn.commit()
        return last_id

    def update_movie(self, id, titel, description, imdb_rating, year):
        self.cursor.execute("""
        UPDATE movies SET title=?, description=?, imdb_rating=?, year=?
        WHERE id=?
        """, (titel, description, imdb_rating, year, id))
        self.conn.commit()

    def get_movie_by_id(self, id):
        self.cursor.execute("""
            SELECT * FROM movies WHERE id=?
        """, (id, ))
        row = self.cursor.fetchone()
        if row is None:
            return None
        return dict(zip(('id', 'title', 'description', 'imdb_rating', 'year'), row))


    def get_all_movies(self):
        self.cursor.execute("""
           SELECT * FROM movies
           """)
        rows = self.cursor.fetchall()
        return [dict(zip(('id', 'title', 'description', 'imdb_rating', 'year'), row)) for row in rows]

    def get_all_movies_across_tables(self):
        self.cursor.execute("""
                SELECT m.id, m.title, m.description, m.imdb_rating, m.year, GROUP_CONCAT(DISTINCT md.director_id) AS directors, GROUP_CONCAT(DISTINCT mg.genre_id) AS genres
                FROM movies as m
                JOIN movie_director as md ON m.id = md.movie_id
                JOIN movie_genre as mg ON m.id = mg.movie_id
                GROUP BY m.id, m.title;
                   """)
        rows = self.cursor.fetchall()
        return [dict(zip(('id', 'title', 'description', 'imdb_rating', 'year', 'directors', 'genres'),
                         (row[0], row[1], row[2], row[3], row[4], [int(d) for d in row[5].split(',')], [int(g) for g in row[6].split(',')]))) for row in rows]

    def get_movie_across_tables_by_id(self, id):
        self.cursor.execute("""
                SELECT m.id, m.title, m.description, m.imdb_rating, m.year, GROUP_CONCAT(DISTINCT md.director_id) AS directors, GROUP_CONCAT(DISTINCT mg.genre_id) AS genres
                FROM movies as m
                JOIN movie_director as md ON m.id = md.movie_id
                JOIN movie_genre as mg ON m.id = mg.movie_id
                WHERE m.id = ?
                GROUP BY m.id, m.title;
                   """, (id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            return [dict(zip(('id', 'title', 'description', 'imdb_rating', 'year', 'directors', 'genres'),
                             (row[0], row[1], row[2], row[3], row[4], [int(d) for d in row[5].split(',')], [int(g) for g in row[6].split(',')])))]

    def get_top10(self):
        self.cursor.execute("""
           SELECT m.id, m.title, m.description, m.imdb_rating, m.year, GROUP_CONCAT(DISTINCT md.director_id) AS directors, GROUP_CONCAT(DISTINCT mg.genre_id) AS genres
                FROM movies as m
                JOIN movie_director as md ON m.id = md.movie_id
                JOIN movie_genre as mg ON m.id = mg.movie_id
                GROUP BY m.id, m.title
                ORDER BY imdb_rating DESC LIMIT 10;
           """)
        rows = self.cursor.fetchall()
        return [dict(zip(('id', 'title', 'description', 'imdb_rating', 'year', 'directors', 'genres'),
                         (row[0], row[1], row[2], row[3], row[4], [int(d) for d in row[5].split(',')],
                          [int(g) for g in row[6].split(',')]))) for row in rows]


    def get_movies_by_year(self, year):
            self.cursor.execute("""
               SELECT * FROM movies
               WHERE year=?""", (year,))
            rows = self.cursor.fetchall()
            return [dict(zip(('id', 'title', 'description', 'imdb_rating', 'year'), row)) for row in rows]

    def get_movies_by_genre(self, genre_id):
        self.cursor.execute("""
           SELECT * FROM movies
           WHERE id IN (
                    SELECT * FROM movie_genre
                    where genre_id=?
                    )    
           """, (genre_id,))
        rows = self.cursor.fetchall()
        return [dict(zip(('id', 'title', 'description', 'imdb_rating', 'year'), row)) for row in rows]

    def search_movies_by_title(self, pattern):
        self.cursor.execute("""
               SELECT *
               FROM movies
               WHERE title LIKE ?
           """, (pattern,))
        rows = self.cursor.fetchall()
        return [dict(zip(('id', 'title', 'description', 'imdb_rating', 'year'), row)) for row in rows]



    def delete_movie(self, id):
        self.cursor.execute("""
            DELETE FROM movies
            WHERE id=?
        """, (id,))
        self.conn.commit()

    def get_last_id(self):
        self.cursor.execute("""
            SELECT id FROM movies ORDER BY id DESC LIMIT 1
        """)
        row = self.cursor.fetchone()
        if row is None:
            return 0
        return row[0]


class GenreDatabase:

    def __init__(self):
        self.conn = sqlite3.connect('movies.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS genres (
                g_id INTEGER PRIMARY KEY,
                genre VARCHAR(255) UNIQUE
            );
        """)

    def add_genre(self, genre):
        g_id = self.get_last_g_id() + 1
        self.cursor.execute("""
            INSERT INTO genres VALUES 
            (?, ?)
        """, (g_id, genre))
        self.conn.commit()
        return g_id

    def update_genre(self, g_id, genre):
        self.cursor.execute("""
        UPDATE genres SET genre=?
        WHERE g_id=?
        """, (genre, g_id))
        self.conn.commit()

    def get_all_genres(self):
        self.cursor.execute("""
           SELECT * FROM genres
           """)
        rows = self.cursor.fetchall()
        return [dict(zip(('g_id', 'genre'), row)) for row in rows]

    def get_genres_by_alphabet(self):
        self.cursor.execute("""
              SELECT * FROM genres
              order by genre
              """)
        rows = self.cursor.fetchall()
        return [dict(zip(('g_id', 'genre'), row)) for row in rows]

    def get_genre_by_id(self, g_id):
        self.cursor.execute("""
            SELECT * FROM genres WHERE g_id=?
        """, (g_id,))
        row = self.cursor.fetchone()
        return dict(zip(('g_id', 'genre'), row))

    def get_genre_id_by_name(self, genre):
        self.cursor.execute("""
            SELECT g_id FROM genres WHERE genre=?
        """, (genre,))
        row = self.cursor.fetchone()
        if row:
            return dict(zip(('g_id',), row))['g_id']
        else:
            return None
        
    def genre_exists(self, genre):
        self.cursor.execute("""
               SELECT * FROM genres WHERE genre=?
           """, (genre, ))
        row = self.cursor.fetchone()
        return row is not None

    def delete_genre(self, g_id):
        self.cursor.execute("""
            DELETE FROM genres
            WHERE g_id=?
        """, (g_id,))
        self.conn.commit()

    def get_last_g_id(self):
        self.cursor.execute("""
            SELECT g_id FROM genres ORDER BY g_id DESC LIMIT 1
        """)
        row = self.cursor.fetchone()
        if row is None:
            return 0
        return row[0]

class DirectorDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('movies.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS directors (
                d_id INTEGER PRIMARY KEY,
                d_name VARCHAR(255),
                d_lname VARCHAR(255)
            );
        """)

    def add_director(self, d_name, d_lname):
        d_id = self.get_last_d_id() + 1
        self.cursor.execute("""
            INSERT INTO directors VALUES 
            (?, ?, ?)
        """, (d_id, d_name, d_lname))
        self.conn.commit()
        return d_id

    def update_director(self, d_id, d_name, d_lname):
        self.cursor.execute("""
        UPDATE directors SET d_name=?, d_lname=?
        WHERE d_id=?
        """, (d_name, d_lname, d_id))
        self.conn.commit()

    def get_directors_order_by_lname(self):
        self.cursor.execute("""
           SELECT * FROM directors
           ORDER BY d_lname
           """)
        rows = self.cursor.fetchall()
        return [dict(zip(('d_id', 'd_name', 'd_lname'), row)) for row in rows]

    def get_all_directors(self):
        self.cursor.execute("""
           SELECT * FROM directors
           """)
        rows = self.cursor.fetchall()
        return [dict(zip(('d_id', 'd_name', 'd_lname'), row)) for row in rows]

    def get_director_by_id(self, d_id):
        self.cursor.execute("""
            SELECT * FROM directors WHERE d_id=?
        """, (d_id,))
        row = self.cursor.fetchone()
        return dict(zip(('d_id', 'd_name', 'd_lname'), row))

    def get_director_by_fullname(self, d_name, d_lname):
        self.cursor.execute("""
            SELECT d_id FROM directors WHERE d_name=? AND d_lname=?
        """, (d_name, d_lname))
        row = self.cursor.fetchone()
        if row:
            return dict(zip(('d_id',), row))['d_id']
        else:
            return None

    def director_exists(self, d_name, d_lname):
        self.cursor.execute("""
               SELECT * FROM directors WHERE d_name=? AND d_lname=?
           """, (d_name, d_lname))
        row = self.cursor.fetchone()
        return row is not None

    def delete_director(self, d_id):
        self.cursor.execute("""
            DELETE FROM directors
            WHERE d_id=?
        """, (d_id,))
        self.conn.commit()

    def get_last_d_id(self):
        self.cursor.execute("""
            SELECT d_id FROM directors ORDER BY d_id DESC LIMIT 1
        """)
        row = self.cursor.fetchone()
        if row is None:
            return 0
        return row[0]

class MovieGenreConnect:
    def __init__(self):
        self.conn = sqlite3.connect('movies.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movie_genre (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  movie_id INTEGER,
                  genre_id INTEGER,
                  FOREIGN KEY (movie_id) REFERENCES movies (id),
                  FOREIGN KEY (genre_id) REFERENCES genres (g_id)
                );
        """)

    def add_reference(self, movie_id, genre_id):
        self.cursor.execute("""
            INSERT INTO movie_genre VALUES 
            (?, ?, ?)
        """, (self.get_last_id() + 1, movie_id, genre_id))
        self.conn.commit()

    def update_reference(self, id, movie_id, genre_id):
        self.cursor.execute("""
        UPDATE movie_genre SET movie_id=?, genre_id=?
        WHERE id=?
        """, (movie_id, genre_id, id))
        self.conn.commit()

    def delete_reference(self, id):
        self.cursor.execute("""
            DELETE FROM movie_genre
            WHERE id=?
        """, (id,))
        self.conn.commit()

    def delete_references_by_movie_id(self, movie_id):
        self.cursor.execute("""
               DELETE FROM movie_genre
               WHERE movie_id=?
           """, (movie_id,))
        self.conn.commit()
        
    def delete_references_by_genre_id(self, genre_id):
        self.cursor.execute("""
               DELETE FROM movie_genre
               WHERE genre_id=?
           """, (genre_id,))
        self.conn.commit()

    def get_genres_by_movie(self, movie_id):
        self.cursor.execute("""
            SELECT g_id, genre FROM movie_genre
            JOIN genres ON movie_genre.genre_id = genres.g_id
            WHERE movie_id=?
           """, (movie_id,))
        rows = self.cursor.fetchall()
        return [dict(zip(('g_id', 'genre'), row)) for row in rows]


    def get_last_id(self):
        self.cursor.execute("""
            SELECT id FROM movie_genre ORDER BY id DESC LIMIT 1
        """)
        row = self.cursor.fetchone()
        if row is None:
            return 0
        return row[0]


class MovieDirectorConnect:

    def __init__(self):
        self.conn = sqlite3.connect('movies.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movie_director (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  movie_id INTEGER,
                  director_id INTEGER,
                  FOREIGN KEY (movie_id) REFERENCES movies (id),
                  FOREIGN KEY (director_id) REFERENCES directors (d_id)
                );
        """)

    def add_reference(self, movie_id, director_id):
        self.cursor.execute("""
            INSERT INTO movie_director VALUES 
            (?, ?, ?)
        """, (self.get_last_id() + 1, movie_id, director_id))
        self.conn.commit()

    def update_reference(self, id, movie_id, director_id):
        self.cursor.execute("""
        UPDATE movie_director SET movie_id=?, director_id=?
        WHERE id=?
        """, (movie_id, director_id, id))
        self.conn.commit()


    def delete_reference(self, id):
        self.cursor.execute("""
            DELETE FROM movie_director
            WHERE id=?
        """, (id,))
        self.conn.commit()

    def get_directos_by_movie(self, movie_id):
        self.cursor.execute("""
            SELECT directors.d_id, directors.d_name || ' ' || directors.d_lname AS d_fullname
            FROM movie_director
            JOIN directors ON movie_director.director_id = directors.d_id
            WHERE movie_id=?
           """, (movie_id,))
        rows = self.cursor.fetchall()
        return [dict(zip(('d_id', 'd_fullname'), row)) for row in rows]

    def get_movies_by_director_id(self, director_id):
        self.cursor.execute("""
            SELECT * FROM movies
            WHERE id IN (
                  SELECT movie_id
                  FROM movie_director 
                  WHERE director_id = ?
                  )
           """, (director_id,))
        rows = self.cursor.fetchall()
        return [dict(zip(('id', 'title', 'description', 'imdb_rating', 'year'), row)) for row in rows]

    def delete_references_by_movie_id(self, movie_id):
        self.cursor.execute("""
               DELETE FROM movie_director
               WHERE movie_id=?
           """, (movie_id,))
        self.conn.commit()

    def delete_references_by_director_id(self, director_id):
        self.cursor.execute("""
               DELETE FROM movie_director
               WHERE director_id=?
           """, (director_id,))
        self.conn.commit()

    def get_last_id(self):
        self.cursor.execute("""
            SELECT id FROM movie_director ORDER BY id DESC LIMIT 1
        """)
        row = self.cursor.fetchone()
        if row is None:
            return 0
        return row[0]

