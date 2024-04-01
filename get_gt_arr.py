import pymongo


def get_gt_val(target_object_id):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.test_user
    collection = db.score
    result = collection.find({"_idUser": target_object_id})

    GT_arr = []
    result = collection.find({"_idUser": target_object_id})
    for doc in result:
        if doc['test'] == 'GT':
            GT_arr.append(tuple([doc['date'], doc['score'].strip('%') ]))
    
    if len(GT_arr) == 0:
        return(tuple(["null", "null"]))
    
    prev_tuple = GT_arr[-1]

    return(prev_tuple)

def get_anx_val(target_object_id):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.test_user
    collection = db.score
    result = collection.find({"_idUser": target_object_id})

    anx_arr = []
    result = collection.find({"_idUser": target_object_id})
    for doc in result:
        if doc['test'] == 'Anxiety':
            anx_arr.append(tuple([doc['date'], doc['score'].strip('%') ]))

    if len(anx_arr) == 0:
        return(tuple(["null", "null"]))

    prev_tuple = anx_arr[-1]

    return(prev_tuple)

def get_dep_val(target_object_id):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.test_user
    collection = db.score
    result = collection.find({"_idUser": target_object_id})
    result_anx = collection.find({"_idUser": target_object_id})

    dep_arr = []
    result = collection.find({"_idUser": target_object_id})
    for doc in result:
        if doc['test'] == 'Depression':
            dep_arr.append(tuple([doc['date'], doc['score'].strip('%') ]))

    if len(dep_arr) == 0:
        return(tuple(["null", "null"]))


    prev_tuple = dep_arr[-1]

    return(prev_tuple)