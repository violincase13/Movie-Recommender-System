from math import sqrt
from sklearn.cluster import KMeans
import numpy as np

#from data import movie_names, movie_genre

#algorithm = 'kMean'

def sim_distance(prefs, person1, person2):
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    if len(si)==0: return 0
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item],2)\
                          for item in si])
    return 1/(1+sqrt(sum_of_squares))


def sim_pearson(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1
    n = len(si)
    if n == 0:
        return 0
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    sum1Sq = sum([pow(prefs[p1][it],2) for it in si]) 
    sum2Sq = sum([pow(prefs[p2][it],2) for it in si])
    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])
    num = pSum-(sum1*sum2/n)
    den = sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den == 0:
        return 0
    return num/den


def topMatches(prefs, person, n=3, similarity=sim_pearson):
    scores = [(round(similarity(prefs,person,other), 2),other) \
              for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

def getRecommendationsK():

    from script import clust_train, prediction_data, train_label
    import statistics as stats
    rankings = []

    clust_train_array = np.array(clust_train)
    kmeans = KMeans(n_clusters=12, random_state=0).fit(clust_train_array)
    print('kmeans.labels_: ',kmeans.labels_)
    #print('len(kmeans.labels_)',len(kmeans.labels_))
    print('prediction_data: ', prediction_data)
    prediction = kmeans.predict(prediction_data)
    print('here is the prediction: ', prediction)

    for i in range(len(kmeans.labels_)):
        if kmeans.labels_[i] == stats.mode(prediction):
            rankings.append(train_label[i])
    print(rankings)
    return rankings

def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]
    return result


def calculateSimilarItems(prefs,n=10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result={}
    
    # Invert the preference matrix to be item-centric
    itemPrefs=transformPrefs(prefs)
    #print("itemPrefs: ", itemPrefs)
    c=0
    
    for item in itemPrefs:
        # Status updates for large datasets
        c+=1
        if c%100==0: print("%d / %d" % (c,len(itemPrefs)))
        # Find the most similar items to this one
        scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
        result[item]=scores

    return result


def getRecommendedItems(prefs,itemMatch,user):
    userRatings=prefs[user]
    #print(userRatings[:10])
    scores={}
    totalSim={}

    # Loop over items rated by this user
    for (item,rating) in userRatings.items():
        # Loop over items similar to this one
        for (similarity,item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings: continue

            # Weighted sum of rating times similarity
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating

            # Sum of all the similarities
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity

    # Divide each total score by total weighting to get an average
    rankings=[(round(score/totalSim[item], 2),item) for item,score in scores.items()]
    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings
