import pymongo
client = pymongo.MongoClient('localhost', 27017)
db = client.test_user
collection = db.score
target_object_id = "2bf8a5c047d8429993f2ea21e65fa44c"
result = collection.find({"_idUser": target_object_id})
result_anx = collection.find({"_idUser": target_object_id})


anx_arr = []
GT_arr =[]
for doc in result:
        if doc['test'] == 'GT':
            GT_arr.append(tuple([doc['date'], doc['score'].strip('%') ]))
for doc_a in result_anx:
        if doc_a['test'] == 'Anxiety':
            anx_arr.append(tuple([doc_a['date'], float(doc_a['score'].strip('%')) ]))

print(GT_arr)
print(anx_arr)