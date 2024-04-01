import pymongo
client = pymongo.MongoClient('localhost', 27017)
db = client.test_user
collection = db.score
result = collection.find({"_idUser": "2bf8a5c047d8429993f2ea21e65fa44c"})


dep_arr = []
result = collection.find({"_idUser": "2bf8a5c047d8429993f2ea21e65fa44c"})
for doc in result:
    if doc['test'] == 'GT':
        dep_arr.append(tuple([doc['date'], doc['score'].strip('%') ]))

for i in range(len(dep_arr)):
    print(f'date: {dep_arr[i][0]}, Score: {dep_arr[i][1]}')