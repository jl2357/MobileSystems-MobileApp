from flask import Flask, render_template, Response
from objRecognition import sessionRecog
app = Flask(__name__)

#rec = sessionRecog()

@app.route('/')
def index():
    return render_template("index.html")    

def gen(objRecognotion):
    while True:
        video_frame = rec.get_frames()
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + video_frame + b'\r\n\r\n')
        
@app.route('/video_feed')
def video_feed():
    return Response(gen(rec),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/session')
def session():
    print("hello")
    return render_template("session.html")

if __name__ == '__main__':
    app.run(debug=True, host= '172.20.10.2')