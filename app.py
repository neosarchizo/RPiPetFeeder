#!/usr/bin/env python
from flask import Flask, render_template, Response
from camera import Camera
import serial

arduino = serial.Serial('/dev/ttyACM0', 9600)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/feed")
def feed():
    try:
        arduino.write('a')
        return "1"
    except:
        pass        

    return "0"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)