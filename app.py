import cv2
import numpy as np
import tensorflow as tf
import time
from flask import Flask, render_template, Response, jsonify

app = Flask(__name__)

# Load the trained emotion detection model
model = tf.keras.models.load_model("emotion_model.h5")

# Emotion labels
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

# Face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Global variables
cap = None
video_capture = False
emotion_counts = {label: 0 for label in emotion_labels}
start_time = None

def detect_emotion(frame):
    """Detects emotion, draws bounding boxes, and updates emotion counts."""
    global emotion_counts
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    detected_emotion = "Neutral"

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (48, 48))
        face = face.astype("float32") / 255.0
        face = np.expand_dims(face, axis=0)
        face = np.expand_dims(face, axis=-1)

        predictions = model.predict(face)
        detected_emotion = emotion_labels[np.argmax(predictions)]
        emotion_counts[detected_emotion] += 1  

        # 🔹 **Fix: Draw green bounding box**
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box

        # 🔹 **Fix: Display detected emotion clearly**
        cv2.putText(frame, detected_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.9, (0, 255, 0), 2)

    return frame  

def generate_frames():
    """Streams video frames, detects emotions, and overlays results."""
    global cap, video_capture, start_time, emotion_counts

    start_time = time.time()
    while video_capture:
        if cap is None or not cap.isOpened():
            break

        success, frame = cap.read()
        if not success:
            continue

        frame = detect_emotion(frame)  # **Fix: Pass frame through emotion detection to modify it**

        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        if time.time() - start_time >= 10:
            video_capture = False
            cap.release()
            cap = None
            break  

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    """Streams video feed."""
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/start", methods=["POST"])
def start_video():
    """Starts the webcam and resets everything."""
    global video_capture, cap, emotion_counts

    if video_capture:  # If already running, do nothing
        return jsonify({"status": "already_running"})

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return jsonify({"status": "error", "message": "Webcam not accessible"}), 500

    video_capture = True
    emotion_counts = {label: 0 for label in emotion_labels}  # Reset emotion counts
    return jsonify({"status": "started"})

@app.route("/result")
def get_result():
    """Returns the dominant emotion and redirects accordingly."""
    global emotion_counts

    # Ensure emotion counts are properly checked
    if not any(emotion_counts.values()):
        final_emotion = "Neutral"
    else:
        final_emotion = max(emotion_counts, key=emotion_counts.get)  # Most detected emotion

    print(f"🔹 Detected Dominant Emotion: {final_emotion}")  # Debugging

    # 🔹 **Fix: Redirect based on the detected emotion**
    if final_emotion in ["Happy", "Neutral"]:
        return jsonify({"redirect": "/funisland"})
    else:  
        return jsonify({"redirect": "/express_yourself"})

@app.route("/funisland")
def funisland():
    return render_template("funisland.html")

@app.route("/express_yourself")
def express_yourself():
    return render_template("express_yourself.html")

if __name__ == "__main__":
    app.run(debug=True)
