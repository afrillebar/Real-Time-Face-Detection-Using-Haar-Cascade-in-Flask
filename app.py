from flask import Flask, render_template, Response
import cv2, time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template ("index.html")

def gen():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
        ret, img = cap.read()
        img = cv2.flip(img,180)
        faces = face_cascade.detectMultiScale(img, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_color = img[y:y+h, x:x+w]
        if ret == True:
            img = cv2.resize(img, (0,0), fx=1, fy=1) 
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        else: 
            break
        
@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)