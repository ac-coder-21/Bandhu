from flask import Flask, render_template, session, redirect, request, jsonify
from functools import wraps
import pymongo
from user.models import User
from datetime import datetime
from bson import ObjectId
from fpdf import FPDF
import time
import html

from GT.chat_gt import get_response
from Anxiety.chat_anx import get_response_anx
from Depression.chat_dep import get_response_dep
from det_que_or_continuation import gmh_questions, anx_questions, dep_questions
import gridfs
from pdf_report import generate_pdf
from get_gt_arr import get_gt_val, get_dep_val, get_anx_val




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
    return render_template('signin.html')

@app.route('/create-account/')
def create_acc():
    return render_template('signup.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.test_user
    collection = db.score
    target_object_id = session['user']['_id']
    result = collection.find({"_idUser": target_object_id})

    result_rev = []
    final_res = []
    null_obj = {'test': '-', 'score': '-'}
    for doc in result:
        print(doc)
        result_rev.append(doc)

    if len(result_rev) == 0:
        for i in range(5):
            final_res.append(null_obj)
        return render_template('dashboard.html', final_res=final_res)

    

    if len(result_rev) == 1:
        for d in result_rev:
            final_res.append(d)
        for i in range(4):
            final_res.append(null_obj)
        return render_template('dashboard.html', final_res=final_res)
    
    result_rev = result_rev[::-1]
    
    if len(result_rev) == 2:
        for d in result_rev:
            final_res.append(d)
        for i in range(3):
            final_res.append(null_obj)
        return render_template('dashboard.html', final_res=final_res)
    
    if len(result_rev) == 3:
        for d in result_rev:
            final_res.append(d)
        for i in range(2):
            final_res.append(null_obj)
        return render_template('dashboard.html', final_res=final_res)
    
    if len(result_rev) == 4:
        for d in result_rev:
            final_res.append(d)
        final_res.append(null_obj)
        return render_template('dashboard.html', final_res=final_res)

    for i in range(5):
        final_res.append(result_rev[i])

    return render_template('dashboard.html', final_res=final_res)

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
@login_required
def predict():
    mongo_uri = "mongodb://localhost:27017/test_user"
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

        current_date = datetime.now()
        formatted_date = current_date.strftime('%d-%m-%Y')

        name = session['user']['name']
        timestamp = time.time()
        file_name = f'{name}-{timestamp}-General Mental Health Assessment.pdf'

        score_data = {
            "_idUser": target_object_id,
            "test": "GT",
            "score": str(precent_resp*100) + '%',
            "date": formatted_date,
            "file_name": file_name
        }

        prev_values =  get_gt_val(target_object_id=target_object_id)

        

        generate_pdf(date=formatted_date, name=session['user']['name'], age=session['user']['age'], gender=session['user']['gender'], education=session['user']['qualification'], test='General Mental Health Assesment', prev_score=prev_values[1], prev_test_date=prev_values[0], score=str(precent_resp*100) + '%', file_name=file_name)

        location = 'D:\Bandhu-A-mental-chatbot-app\\' + file_name
        file_Data = open(location, 'rb')
        data = file_Data.read()
        fs = gridfs.GridFS(db)
        fs.put(data=data, filename = file_name)

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
        
        


    else:
        output = get_response(text)
        message = {"output": output}
        return jsonify(message)
    
@app.route('/gt/ui')
@login_required
def gt_ui():
    return render_template('gt.html')


@app.post("/anxiety")
@login_required
def predict_anx():
    mongo_uri = "mongodb://localhost:27017/test_user"
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

        current_date = datetime.now()
        formatted_date = current_date.strftime('%d-%m-%Y')

        score_data = {
            "_idUser": session['user']['_id'],
            "test": "Anxiety test",
            "score": str(precent_resp*100) + '%',
            "date": formatted_date
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
@login_required
def anxiety_ui():
    return render_template('anxiety.html')


@app.post("/depression")
@login_required
def predict_dep():
    mongo_uri = "mongodb://localhost:27017/test_user"
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

        current_date = datetime.now()
        formatted_date = current_date.strftime('%d-%m-%Y')

        score_data = {
            "_idUser": session['user']['_id'],
            "test": "Anxiety test",
            "score": str(precent_resp*100) + '%',
            "date": formatted_date
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
        output = get_response_dep(text)
        message = {"output": output}
        return jsonify(message)
    
@app.route('/depression/ui/')
@login_required
def depression_ui():
    return render_template('depression.html')

@app.route('/score_graph/')
@login_required
def score_graph():

    client = pymongo.MongoClient('localhost', 27017)
    db = client.test_user
    collection = db.score
    target_object_id = session['user']['_id']
    result = collection.find({"_idUser": target_object_id})
    result_anx = collection.find({"_idUser": target_object_id})
    result_dep = collection.find({"_idUser": target_object_id})



    GT_arr = []
    anx_arr = []
    dep_arr = []
    for doc in result:
        if doc['test'] == 'GT':
            GT_arr.append(tuple([doc['date'], doc['score'].strip('%') ]))
    
    for doc_a in result_anx:
        if doc_a['test'] == 'Anxiety':
            anx_arr.append(tuple([doc_a['date'], float(doc_a['score'].strip('%')) ]))

    for doc_d in result_dep:
        if doc_d['test'] == 'Depression':
            dep_arr.append(tuple([doc_d['date'], float(doc_d['score'].strip('%')) ]))

    decoded_GT_arr = [(html.unescape(date), html.unescape(value)) for date, value in GT_arr]
    decoded_anx_arr = [(html.unescape(date_anx), html.unescape(str(value_anx))) for date_anx, value_anx in anx_arr]
    decoded_dep_arr = [(html.unescape(date_dep), html.unescape(str(value_dep))) for date_dep, value_dep in dep_arr]

    GT_labels = [row[0] for row in GT_arr]
    GT_values = [row[1] for row in GT_arr]
    

    Anxiety_labels = [row[0] for row in anx_arr]
    Anxiety_values = [row[1] for row in anx_arr]

    Depression_labels = [row[0] for row in dep_arr]
    Depression_values = [row[1] for row in dep_arr]

    return render_template('graph_hist.html', decoded_dep_arr = decoded_dep_arr,decoded_anx_arr=decoded_anx_arr,decoded_GT_arr=decoded_GT_arr,GT_labels=GT_labels, GT_values=GT_values, Anxiety_labels=Anxiety_labels, Anxiety_values=Anxiety_values, Depression_labels=Depression_labels, Depression_values= Depression_values)



if __name__ == "__main__":
    app.run(debug=True)