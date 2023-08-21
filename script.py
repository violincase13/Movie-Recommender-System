import csv
from kmeandata import user_genresK

print("-------1-----------")
print('user_g from script: ', user_genresK)
print("--------2----------")
'''# script to add columns inside data for (genre, cover)
with open('outputdataset.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        print(type(eval(row['genre'])))'''
genre_set = set()
clust_train = []

train_label = []
user_predict = []
prediction_data = []
genre_list = []



# script to modify the type of genre
with open('output_dataset.csv', mode='r', encoding="latin-1") as csv_file:  
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        #try:
        #print(row['genre'])
        aux = eval(row['genre'])
        #print(type(aux))
        genre_list = set(aux)
        #print(genre_list)
        genre_set = genre_set.union(genre_list)
        #print(genre_set)
        #except Exception:
        #    pass

genre_list = list(genre_set)
genre_list.sort()
print('genre_list: ', genre_list)

with open('output_dataset.csv', mode='r', encoding="latin-1") as csv_file:  
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data = [eval(row['userID'])] #modified smth here
        for genre in genre_list:
            if genre in row['genre']:
                data.append(1)
            else:
                data.append(0)
        while len(row['imdbID'])< 7:	
            row['imdbID'] = '0'+ row['imdbID']
        train_label.append(row['imdbID'])
        clust_train.append(data)
        #print(clust_train)

#print('cluster_train: ', clust_train)   <-  this is from database   
print('user_genresk script: ', user_genresK)
print('user_genresk script (val): ', user_genresK.values())
for genres in user_genresK.values():
    print("user_genresk.values()", user_genresK.values())

    user_predict =[]
    user_predict.append(0) # this will be the number of the critic
    for genre in genre_list:
        if genre in genres:
            user_predict.append(1)
        else:
            user_predict.append(0)
    prediction_data.append(user_predict)

print('prediction data: ', prediction_data)
    
    

#print(len(clust_train))
#print(clust_train) #gresit

#print("The prediction is: " + str(prediction_data))
#print(len(prediction_data))
#print(prediction_data)