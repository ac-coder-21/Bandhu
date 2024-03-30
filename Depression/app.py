from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from chat_dep import get_response_dep
from det_que_or_continuation import dep_questions
from bson import ObjectId
from fpdf import FPDF

app = Flask(__name__)
CORS(app)

@app.post("/depression")
def predict():
    mongo_uri = "mongodb://localhost:27017/test_mc"
    client = pymongo.MongoClient(mongo_uri)
    db = client.test_mc
    collection = db.Project

    target_object_id = ObjectId("65e4267c064e0a1420a3c6c5")

    document = collection.find_one({"_id": target_object_id})
    if document is None:
        return jsonify({"error": "Document with id 1 not found"})
    
    user_response_arr = []

    text = request.get_json().get("message")
    val = document["val"]

    response_old = document["score"]




    if str(text).lower() == 'no':
        message = {"output": "Okay no problem, feel free to start the test whenever you want to, I am always here for you"}
        return jsonify(message)

    elif str(text).lower() == 'yes':
        new_data_value = val+1
        question = dep_questions[val]
        result = collection.update_one({"_id": target_object_id}, {"$set": {"val": new_data_value}})
        if result.modified_count > 0:
            message = {"output": question}
        else:
            message = {"output": "Data attribute not updated"}
        return jsonify(message)
    
    
    

    elif val > 0 and val < 11:
        new_data_value = val+1
        
        result = collection.update_one({"_id": target_object_id}, {"$set": {"val": new_data_value}})
        res = request.get_json().get("message")


        resp = get_response_dep(res)

        resp_arr = resp.split('.')
        resp_score = int(resp_arr[0])
        if resp_score != 2:
            response_old += resp_score

        question = resp_arr[1]
        question += '.Next question:' + dep_questions[val]
        if result.modified_count > 0:
            message = {"output": question}
        else:
            message = {"output": "Data attribute not updated"}

        collection.update_one({"_id": target_object_id}, {"$set": {"score": response_old}})

        return jsonify(message)
    


    elif val >=11:
        new_data_value = 0
        print(user_response_arr)
        result = collection.update_one({"_id": target_object_id}, {"$set": {"val": new_data_value}})

        res = request.get_json().get("message")

        resp = get_response_dep(res)

        resp_arr = resp.split('.')
        resp_score = int(resp_arr[0])
        if resp_score != 2:
            response_old += resp_score

        response_old += resp_score

        collection.update_one({"_id": target_object_id}, {"$set": {"score": 0}})

        precent_resp = response_old/12

        score = db.score

        score_data = {
            "_idUser": ObjectId("65e4267c064e0a1420a3c6c5"),
            "test": "Anxiety test",
            "score": str(precent_resp*100) + '%'
        }

        score.insert_one(score_data)

        if precent_resp >= 0.60 and precent_resp<0.75:
            message = {"output": 'I would like you to listen to music and watch comedy videos as laughter is best medicine. Try to stay away from social media as it have negativity'}
            return jsonify(message)
        
        elif precent_resp >= 0.75 and precent_resp < 0.9:
            message = {"output": "Read books about mental stability. I would recommend 'An UnQuiet mind' and 'All alone with you'. I would also like you to meditate for a hour. Breating exercises and yoga are way to go!!"}
        
        elif precent_resp >= 0.9:
            message = {"output": 'Have mental problems is something that everyone goes through it!! I would recommend you to visit a nearby therapist for consultancy, dont be sad as this time shall also pass. Tele manas is an Indian govt initiative for mental help, Please feel free to contact: 1-800 891 4416'}
            return jsonify(message)

        else:
            message = {"output": 'low'}
            return jsonify(message)
        

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('helvetica', "", 10)

        
        


    else:
        output = get_response_dep(text)
        message = {"output": output}
        return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
