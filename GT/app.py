

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pymongo
# from chat import get_response
# from det_que_or_continuation import gmh_questions
# from bson import ObjectId

# app = Flask(__name__)
# CORS(app)

# @app.post("/gt")
# def predict():
#     mongo_uri = "mongodb://localhost:27017/test_mc"
#     client = pymongo.MongoClient(mongo_uri)
#     db = client.test_mc
#     collection = db.Project

#     target_object_id = ObjectId("65e4267c064e0a1420a3c6c5")

#     document = collection.find_one({"_id": target_object_id})
#     if document is None:
#         return jsonify({"error": "Document with id 1 not found"})
    
#     user_response_arr = []

#     text = request.get_json().get("message")
#     val = document["val"]

#     response_old = document["score"]

#     if str(text).lower() == 'yes':
#         new_data_value = val+1
#         question = gmh_questions[val]
#         result = collection.update_one({"_id": target_object_id}, {"$set": {"val": new_data_value}})
#         if result.modified_count > 0:
#             message = {"output": question}
#         else:
#             message = {"output": "Data attribute not updated"}
#         return jsonify(message)
    

#     elif val > 0 and val < 10:
#         new_data_value = val+1
#         question = gmh_questions[val]
#         result = collection.update_one({"_id": target_object_id}, {"$set": {"val": new_data_value}})
#         if result.modified_count > 0:
#             message = {"output": question}
#         else:
#             message = {"output": "Data attribute not updated"}
        
#         resp = int(request.get_json().get("message"))
#         response_old += resp

#         collection.update_one({"_id": target_object_id}, {"$set": {"score": response_old}})

#         return jsonify(message)
    

#     elif val >=10:
#         new_data_value = 0
#         print(user_response_arr)
#         result = collection.update_one({"_id": target_object_id}, {"$set": {"val": new_data_value}})

#         resp = int(request.get_json().get("message"))
#         response_old += resp

#         collection.update_one({"_id": target_object_id}, {"$set": {"score": 0}})

#         precent_resp = response_old/40

#         score = db.score

#         score_data = {
#             "_idUser": ObjectId("65e4267c064e0a1420a3c6c5"),
#             "test": "General Mental Health assessment test",
#             "score": str(precent_resp*100) + '%'
#         }

#         score.insert_one(score_data)

#         if precent_resp >= 0.75 and precent_resp<0.9:
#             output = get_response("detected general mental test")
#             message = {"output": output}
#             return jsonify(message)
        
#         elif precent_resp >= 0.9:
#             output = get_response("severe general mental test")
#             message = {"output": output}
#             return jsonify(message)

#         else:
#             output = get_response("undetected general mental test")
#             message = {"output": output}
#             return jsonify(message)
        
        


#     else:
#         output = get_response(text)
#         message = {"output": output}
#         return jsonify(message)

# if __name__ == "__main__":
#     app.run(host='127.0.0.1', port=5353, debug=True )
