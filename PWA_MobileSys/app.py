# imports
from flask import Flask, render_template, Response, request, send_file, jsonify
from objRecognition import sessionRecog
import base64
from PIL import Image
import io
from uuid import uuid1
from database import db
from loginVerification import loginVerify

# initialised objects
rec = sessionRecog()
hours = 0
minutes = 0

# creating an instance of flask
app = Flask(__name__)

# routes
@app.route('/')
def index():
    return render_template("index.html")   

# manifest json route 
@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

# sw route 
@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

# inserting new users used in Postman platform only
@app.route('/users', methods=['POST'])
def users():
    collection = db.User_Logins

    # generate a unique uid string
    _id = str(uuid1().hex)

    # python dictionaries are used to store values in pairs
    data = {
        "_id": _id,
        "username": "admin",
        "password": "admin"
    }

    
   
    # insert data into db
    result = collection.insert_one(data)
    return render_template('home.html')

# post the hours and minutes from the timer, return the session.html
@app.route('/session', methods=['POST'])
def session():
    global hours 
    global minutes
    hours = request.form['hours']
    minutes = request.form['minutes']

    return render_template("session.html")

# get the duration of the session
@app.route('/getDuration', methods=['GET'])
def getDuration():
    
    duration = {'hours':hours, 'minutes':minutes}
    return jsonify(duration)

# get the JSON object for detection results
@app.route('/getDetect', methods=['GET'])
def getDetect():
    return rec.getDetected()

# send frames for processing
@app.route('/process_frames', methods=['POST'])
def process_frames():
    data = request.get_json()
    recieved_img = data['image'].split(",")[1]

    img_data = base64.b64decode(recieved_img)
    img = Image.open(io.BytesIO(img_data))
    
    rec.detect_obj(img)

    return("Image passed through to python!")

# route to home.html
@app.route('/home')
def home():
    return render_template("home.html")

# send inputted login details and verify login in backend model
@app.route('/verifyLogin', methods=['POST'])
def verifyLogin():
    verified = loginVerify.verifyUser(db, request.form['username'], request.form['password'])
    if verified:
        return render_template("home.html") 
    else:
        return render_template("index.html")

# route to render session timer page
@app.route('/sessionTimerSetup')
def sessionTimerSetup():
    return render_template("sessionTimerSetup.html")

# route to render session failed page
@app.route('/sessionFailed')
def sessionFailed():
    return render_template("sessionFailed.html")

# route to render session success page
@app.route('/sessionSuccess')
def sessionSuccess():
    return render_template("sessionSuccess.html")

# route to render planet library page
@app.route('/planetsLibrary')
def planetsLibrary():
    return render_template("planetsLibrary.html")

# route to render history page
@app.route('/history')
def history():
    return render_template("history.html")

# main
if __name__ == '__main__':
    # address at home: 192.168.1.150
    # address at home: 172.20.10.2
    # please change the host name to the device's ipv4 address
    app.run(debug=True, host='192.168.1.150', port=5500) 



