import csv
import requests
from bs4 import BeautifulSoup

movie_names = {} # {imdbID: title, ...}
critics = {}     # {usedID: {imdbID: float(rating), ...}, ...}

with open('dataset.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        movie_names[row['imdbID']] = row['title']

        critics.setdefault(row['userID'], {})
        critics[row['userID']][row['imdbID']] = float(row['rating'])

def get_ratings(url: str) -> dict:
    "Parses user ratings list and return users rating dict"

    user_ratings = {}   # {imdbID: float(rating), ...}

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

    # adding to user_ratings
    for i in range(len(id_list)):
        imdbID = id_list[i]
        rating = float(ratings_list[i])
        user_ratings[imdbID] = rating

    return user_ratings
