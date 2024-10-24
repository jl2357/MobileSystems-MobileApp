from flask import Flask, render_template, Response, request, send_file, jsonify
from objRecognition import sessionRecog
import base64
from PIL import Image
import io
app = Flask(__name__)

# initialised objects
rec = sessionRecog()
hours = 0
minutes = 0

# routes
@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/')
def index():
    return render_template("index.html")    

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
    app.run(debug=True, host= '192.168.1.150', port= 5500) 