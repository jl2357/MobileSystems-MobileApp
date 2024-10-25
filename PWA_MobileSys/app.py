from flask import Flask, render_template, Response, request, send_file, jsonify
from objRecognition import sessionRecog
import base64
from PIL import Image
import io
from uuid import uuid1
from pymongo import MongoClient
from loginVerification import loginVerify
# initialised objects
rec = sessionRecog()
hours = 0
minutes = 0

#app.config["MONGO_URI"] = "mongodb+srv://jennylim366:SQvHmwOU1YdaffWS@cluster0.jxrnw.mongodb.net/MobileSystems?retryWrites=true"
client = MongoClient('127.0.0.1', 27017)
db = client.MobileSys_PWA

# creating an instance of flask
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")   
# routes
@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')



# inserting new users
@app.route('/users', methods=['POST'])
def users():
    collection = db.User_Logins

    # generate a unique uid string
    _id = str(uuid1().hex)

    # python dictionaries are used to store values in pairs
    data = {
        "_id": _id,
        "username": "admin2",
        "password": "admin22"
    }

    print("in the post function")
   
    # insert data into db
    result = collection.insert_one(data)
    return render_template('home.html')

@app.route('/session', methods=['POST'])
def session():
    global hours 
    global minutes
    hours = request.form['hours']
    minutes = request.form['minutes']

    print(hours + " " + minutes)
    return render_template("session.html")

@app.route('/getDuration', methods=['GET'])
def getDuration():
    
    print(str(hours) + " " + str(minutes))
    duration = {'hours':hours, 'minutes':minutes}
    return jsonify(duration)

@app.route('/getDetect', methods=['GET'])
def getDetect():
    return rec.getDetected()

@app.route('/process_frames', methods=['POST'])
def process_frames():
    data = request.get_json()
    recieved_img = data['image'].split(",")[1]

    img_data = base64.b64decode(recieved_img)
    img = Image.open(io.BytesIO(img_data))
    
    print(rec.detect_obj(img))
    

    return("Image passed through to python!")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/verifyLogin', methods=['POST'])
def verifyLogin():
    verified = loginVerify.verifyUser(db, request.form['username'], request.form['password'])
    if verified:
        return render_template("home.html") 
    else:
        return render_template("index.html")

@app.route('/sessionTimerSetup')
def sessionTimerSetup():
    return render_template("sessionTimerSetup.html")

@app.route('/sessionFailed')
def sessionFailed():
    return render_template("sessionFailed.html")

@app.route('/sessionSuccess')
def sessionSuccess():
    return render_template("sessionSuccess.html")

@app.route('/planetsLibrary')
def planetsLibrary():
    return render_template("planetsLibrary.html")

@app.route('/history')
def history():
    return render_template("history.html")

if __name__ == '__main__':
    # address at home: 192.168.1.150
    app.run(debug=True, host='192.168.1.150', port=5500) 



