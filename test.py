
import requests

list = [{"title": "The Forbidden Forest", "description": "A group of friends embark on a camping trip in a mysterious forest that's said to be cursed.", "imdb_rating": 7.1, "director": [1, 4], "genre": [2, 3, 5], "year": 2021}, {"title": "The Time Machine", "desc...

url = 'http://127.0.0.1:5000/api/movies'
for i in list:
    data = requests.post(url, i)