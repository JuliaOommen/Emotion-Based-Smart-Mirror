# 🪞 Emotion-Based Smart Mirror

A real-time smart mirror web app, inspired by the movie 'Inside Out', that detects user emotions via webcam using deep learning, overlays expressive emojis, and redirects users to different interactive pages based on their mood. Ideal for fun, mental wellness, and daily motivation.

---

## 🚀 Features

- 🎭 **Real-Time Emotion Detection** using TensorFlow CNN model  
- 📸 **Webcam Capture with OpenCV**  
- 😊 **Emoji Overlay** on faces in live video feed  
- 🔁 **Emotion-Based Redirection** after 10 seconds:  
  - 😀 Happy & 🙂 Neutral → Fun Activities Page  
  - 😞 Sad & 😠 Angry → Express Yourself Diary Page  
- 🎨 **Emotion-Based Filters**  
- 🌤️ **Morning Weather Updates** (via OpenWeatherMap API)  
- 💬 **Daily Inspirational Quotes**  
- 🖼️ **Auto-Generated Captions** based on detected mood  

---

## 📁 Project Structure
emotion_smart_mirror/
├── app.py # Flask backend
├── templates/
│ ├── index.html # Home with webcam start
│ ├── funisland.html # Redirect if happy/neutral
│ ├── express_yourself.html # Redirect if sad/angry
│ ├── past_entries.html # View past diary entries
├── static/
│ └── emojis/ # Emoji image overlays
├── emotion_model.h5 # Trained CNN model
├── requirements.txt # Python dependencies
└── README.md # Project documentation

## 🛠️ Installation

### Install dependencies
pip install -r requirements.txt

### Run the app
python app.py

### Open your browser and navigate to:
http://localhost:5000

---

##🤖 Model Info
CNN-based emotion classifier trained on labeled facial expression datasets.

Recognizes the following emotions:
😠 Angry
😀 Happy
😢 Sad
😐 Neutral
Model file: emotion_model.h5
