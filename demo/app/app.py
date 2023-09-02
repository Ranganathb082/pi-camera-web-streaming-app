#!/usr/bin/env python
from importlib import import_module
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import time
import io
import subprocess
import os
from flask import Flask, render_template, Response, request, send_file, jsonify,  redirect,  send_from_directory
from send_mail import send_mail
# Pins where we have connected servos
#servo_pin = 26          
servo_pin = 19


GPIO.setmode(GPIO.BCM)      # We are using the BCM pin numbering
# Declaring Servo Pins as output pins
GPIO.setup(servo_pin, GPIO.OUT)     
#GPIO.setup(servo_pin1, GPIO.OUT)


# Created PWM channels at 50Hz frequency
p = GPIO.PWM(servo_pin, 50)
#p1 = GPIO.PWM(servo_pin1, 50)
 
# Initial duty cycle
p.start(0)
#p1.start(0)

# import camera driver. Otherwise use pi camera by default
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_pi import Camera

import utils


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/')
def index():

    """Video streaming home page."""
    return render_template('index.html')

streaming = True
def gen(camera):
    """Video streaming generator function."""
    global streaming
    if streaming:
        while streaming:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    
    res = Response(gen(Camera()),mimetype='multipart/x-mixed-replace; boundary=frame')
    return res


@app.route('/servo', methods=['POST'])
def servo():
    slider1 = request.form.get('slider1')
    p.ChangeDutyCycle(float(slider1))
    sleep(1)
    p.ChangeDutyCycle(0)
    redirect_url = '/'
    return jsonify(redirect=redirect_url)

camera_thread = None

@app.route('/capture', methods=['GET', 'POST'])
def capture():
    global camera_thread  # Access the global camera thread variable
    utils.write_boolean_to_file("camera_state", False)
    filename = f"captured_image_{int(time.time())}.jpg"
    
    cmd = f"raspistill --nopreview -t 1 -o {filename}"
    
    try:
        # Stop the camera thread if it's running
        if camera_thread is not None and camera_thread.is_alive():
            camera_thread.stop()  # You should use a more graceful way to stop the thread

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        send_mail(filename)
        if process.returncode == 0:
            # Start the camera thread again after capturing the image
            camera_thread = threading.Thread(target=gen, args=(Camera(),))
            camera_thread.daemon = True
            camera_thread.start()

            return send_file(filename, mimetype='image/jpg')
        else:
            response = {
                "message": "Error capturing image",
                "command": cmd,
                "error": stderr.decode("utf-8")
            }
   
        redirect_url = '/'
        return jsonify(request.referrer, image_link=filename)
    except Exception as e:
        return jsonify(error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', threaded=True)
