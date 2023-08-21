import csv
import requests
import json
from bs4 import BeautifulSoup
from imdb import Cinemagoer

imdb = Cinemagoer()

movie_namesK = {} # {imdbID: title, ...}
criticsK = {}     # {userID: {imdbID: float(rating), ...}, ...}
movie_genresK = {} # genres of every movie in DB ------------------------- s
user_genresK = {} # the genres of user
movie_postersK = {}

#header = ['userID', 'imdbID', 'title', 'rating', 'genre', 'cover']


with open('output_dataset.csv', mode='r', encoding="latin-1") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        while len(row['imdbID'])< 7:	
            row['imdbID'] = '0'+ row['imdbID']
        movie_namesK[row['imdbID']] = row['title']
        movie_genresK[row['imdbID']] = row['genre']
        movie_postersK[row['imdbID']] = row['cover']

        criticsK.setdefault(row['userID'], {})
        criticsK[row['userID']][row['imdbID']] = float(row['rating'])

print('Done!')

def get_ratings_genre(url: str) -> dict:
    "Parses user ratings list and return users rating dict"

    user_ratingsK = {}   # {imdbID: float(rating), ...}

    id_list = []
    ratings_list = []

    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    
    # finding imdbIDs
    divs = soup.find_all("div", class_="lister-item-content")
    for div in divs:
        link = div.find("h3").find("a")["href"]
        imdbID = link.split('/')[2][2:]
        id_list.append(imdbID)
        
    # finding ratings
    divs = soup.find_all("div", class_="ipl-rating-star ipl-rating-star--other-user small")
    for div in divs:
        rating = div.find("span", class_="ipl-rating-star__rating").contents[0]
        ratings_list.append(rating)

    # finding genre
    #print('Algorithm is KMean')
    for i in range(len(id_list)):
        #print("id_list[i]: ", id_list[i])
        genre = imdb.get_movie(id_list[i])
        print(genre['genre'])
        user_genresK[id_list[i]] = genre['genre']
    print("user_genresk from kmeandata: ", user_genresK)
    print('from kmeandata - user_genres: ', user_genresK)

    # adding to user_ratings
    for i in range(len(id_list)):
        imdbID = id_list[i]
        rating = float(ratings_list[i])
        user_ratingsK[imdbID] = rating

    return user_ratingsK, user_genresK
