from flask import Flask, render_template, Response, request, send_file
from objRecognition import sessionRecog
import base64
from PIL import Image
import io
app = Flask(__name__)

# initialised objects
rec = sessionRecog()



# routes
@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

@app.route('/')
def index():
    return render_template("index.html")    

@app.route('/session')
def session():
    print("hello")
    return render_template("session.html")

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

if __name__ == '__main__':
    app.run(debug=True, host= '192.168.1.150', port= 5500) 