from flask import Flask, render_template, Response
import cv2
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    rand_num = random.randint(1, 10) # toto potrebuju sdilet na server real-time
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes() # a toto uz se sdili pres tuhle dalsi yield function, ktera pres video_feed posila primo na src obrazku v html
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)