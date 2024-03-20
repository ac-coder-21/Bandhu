from flask import Flask, render_template, session, redirect, request, jsonify
from functools import wraps
import pymongo
from user.models import User

from GT.chat_gt import get_response
from Anxiety.chat_anx import get_response_anx
from det_que_or_continuation import gmh_questions, anx_questions
from bson import ObjectId
from fpdf import FPDF





app = Flask(__name__)
app.secret_key = b'\xca\xfc\x17\xbd\xda\x15\xf9\x16[\xc2\x08\xbaP\x8d\xf8\xa1'

client = pymongo.MongoClient('localhost', 27017)
db = client.test_user

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/users/signup', methods = ['POST'])
def signup():
    return User().signup()

@app.route('/user/login', methods = ['POST'])
def login():
    return User().login()

@app.route('/user/signout')
def signout():
    return User().signout()

@app.post("/gt")
def predict():
    mongo_uri = "mongodb://localhost:27017/test_mc"
    client = pymongo.MongoClient(mongo_uri)
    db = client.test_user
    collection = db.users

    pdf = FPDF()


    target_object_id = session['user']['_id']

    document = collection.find_one({"_id": target_object_id})
    if document is None:
        return jsonify({"error": "Document with id 1 not found"})
    
    user_response_arr = []

    text = request.get_json().get("message")
    val = document["val"]

    response_old = document["score"]

    if str(text).lower() == 'yes':
        new_data_value = val+1
        question = gmh_questions[val]
        result = collection.update_one({"_id": target_object_id}, {"$set": {"val": new_data_value}})
        if result.modified_count > 0:
            message = {"output": question}
        else:
            message = {"output": "Data attribute not updated"}
        return jsonify(message)
    

    elif val > 0 and val < 10:
        new_data_value = val+1
        question = gmh_questions[val]
        result = collection.update_one({"_id": target_object_id}, {"$set": {"val": new_data_value}})
        if result.modified_count > 0:
            message = {"output": question}
        else:
            message = {"output": "Data attribute not updated"}
        
        resp = int(request.get_json().get("message"))
        response_old += resp

        collection.update_one({"_id": target_object_id}, {"$set": {"score": response_old}})

        return jsonify(message)
    

    elif val >=10:
        new_data_value = 0
        print(user_response_arr)
        result = collection.update_one({"_id": target_object_id}, {"$set": {"val": new_data_value}})

        resp = int(request.get_json().get("message"))
        response_old += resp

        collection.update_one({"_id": target_object_id}, {"$set": {"score": 0}})

        precent_resp = response_old/40

        score = db.score

        score_data = {
            "_idUser": target_object_id,
            "test": "General Mental Health assessment test",
            "score": str(precent_resp*100) + '%'
        }

        score.insert_one(score_data)

        if precent_resp >= 0.75 and precent_resp<0.9:
            output = get_response("detected general mental test")
            message = {"output": output}
            return jsonify(message)
        
        elif precent_resp >= 0.9:
            output = get_response("severe general mental test")
            message = {"output": output}
            return jsonify(message)

        else:
            output = get_response("undetected general mental test")
            message = {"output": output}
            return jsonify(message)
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "", 10)
        
        


    else:
        output = get_response(text)
        message = {"output": output}
        return jsonify(message)
    
@app.route('/gt/ui')
def gt_ui():
    return render_template('gt.html')


@app.post("/anxiety")
def predict_anx():
    mongo_uri = "mongodb://localhost:27017/test_mc"
    client = pymongo.MongoClient(mongo_uri)
    db = client.test_user
    collection = db.users

    target_object_id = session['user']['_id']

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
        question = anx_questions[val]
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


        resp = get_response_anx(res)

        resp_arr = resp.split('.')
        resp_score = int(resp_arr[0])
        if resp_score != 2:
            response_old += resp_score

        question = resp_arr[1]
        question += '.Next question:' + anx_questions[val]
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

        resp = get_response_anx(res)

        resp_arr = resp.split('.')
        resp_score = int(resp_arr[0])
        if resp_score != 2:
            response_old += resp_score

        response_old += resp_score

        collection.update_one({"_id": target_object_id}, {"$set": {"score": 0}})

        precent_resp = response_old/12

        score = db.score

        score_data = {
            "_idUser": session['user']['_id'],
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
        
        


    else:
        output = get_response_anx(text)
        message = {"output": output}
        return jsonify(message)

@app.route('/anxiety/ui')
def anxiety_ui():
    return render_template('anxiety.html')


if __name__ == "__main__":
    app.run(debug=True)