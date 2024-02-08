from flask import Flask, render_template, Response
import cv2
from pyzbar.pyzbar import decode
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    used_codes = []

    while True:
        success, frame = cap.read()

        for code in decode(frame):
            if code.data.decode('utf-8') not in used_codes:
                print('Approved. The item has been registered')
                print(code.data.decode('utf-8'))
                used_codes.append(code.data.decode('utf-8'))
                time.sleep(5)
            elif code.data.decode('utf-8') in used_codes:
                print('Sorry, the item has been registered')
                time.sleep(5)
            else:
                pass

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
