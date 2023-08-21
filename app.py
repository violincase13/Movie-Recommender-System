from flask import Flask, render_template, request
from data import movie_genres, movie_posters
#from data import *
from kmeandata import movie_namesK, movie_genresK, movie_postersK,criticsK,get_ratings_genre
from data import movie_names, movie_genres, movie_posters,critics, get_ratings
from recommendationsP import getRecommendationsP
from recommendationsK import getRecommendationsK

app = Flask(__name__)

def perform_training(algorithm):
        results = {}
        
        # find imdb url
        url = request.form.get("ratings-url")

        # run getRecommendations
        if algorithm == "pearson":

            # parse ratings for pearson
            ratings_pearson = get_ratings(url)
            critics["user"] = ratings_pearson

            results = getRecommendationsP(critics, "user") 
            results = {score: imdbID for score, imdbID in results if score > 3}
            print(results)

        elif algorithm == "kmean":

            # parse ratings for kmean
            ratings_kmean = get_ratings_genre(url)
            criticsK["user"] = ratings_kmean

            results = getRecommendationsK() 
            import random
            print(1)
            #import pdb; pdb.set_trace()
            import numpy as np
            
            keys = random.sample(list(np.round(np.arange(4, 5,0.0004),2)), len(results))
            values = random.sample(results, len(results))
            results = dict(zip(keys, values))
            #import pdb; pdb.set_trace()
            print(results) 

        return results  

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/showprediction', methods=['POST'])
def showprediction():
    ml_algorithms = request.form.get('ml_algorithms')
    results = perform_training(ml_algorithms)
    import copy
    #movie_namesK = copy.deepcopy(movie_names)
    #movie_genresK = copy.deepcopy(movie_genres)
    #movie_postersK = copy.deepcopy(movie_posters)
    print("-----------------------------------------------------------------------------------------------------------")
    #print(results)yp
    with open("results.txt", "a") as f:
    #f.write(print(results))
        print('results:', results, file=f)
    #print("-----------------------------------------------------------------------------------------------------------")
    with open("movie_names.txt", "a") as f:
    #f.write(print(results))
        print('movie_names:', movie_names, file=f)
    #print("movie_names",movie_names)
    #print("-----------------------------------------------------------------------------------------------------------")
    with open("movie_genres.txt", "a") as f:
    #f.write(print(results))
        print('movie_genres:', movie_genres, file=f)
    #print("movie_genres",movie_genres)
    with open("movie_posters.txt", "a") as f:
    #f.write(print(results))
        print('movie_posters:', movie_posters, file=f)
    #print("-----------------------------------------------------------------------------------------------------------")
    #print("movie_posters",movie_posters)
    #print("-----------------------------------------------------------------------------------------------------------")
    with open("movie_namesK.txt", "a") as f:
    #f.write(print(results))
        print('movie_namesK:', movie_namesK, file=f)
    #print("movie_namesK",movie_namesK)
    #print("-----------------------------------------------------------------------------------------------------------")
    with open("movie_genresK.txt", "a") as f:
    #f.write(print(results))
        print('movie_genresK:', movie_genresK, file=f)
    #print("movie_genresK",movie_genresK)
    #print("-----------------------------------------------------------------------------------------------------------")
    with open("movie_postersK.txt", "a") as f:
    #f.write(print(results))
        print('movie_postersK:', movie_postersK, file=f)
    #print("movie_postersK",movie_postersK)
    #print("-----------------------------------------------------------------------------------------------------------")
    
    #import copy


    return render_template('index.html', results=results, movie_names=movie_names, movie_genres=movie_genres, movie_posters=movie_posters, movie_namesK=movie_namesK, movie_genresK=movie_genresK, movie_postersK=movie_postersK)

if __name__ == "__main__":
    app.run(debug=True)