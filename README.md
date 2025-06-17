Virtual Keyboard with Hand Tracking

This project implements a **virtual keyboard** using real-time **hand tracking** powered by **MediaPipe** and **OpenCV**. Users can type and interact with a virtual keyboard displayed on screen using only their hand gestures — no physical keyboard required.

---

Features:

-Real-time hand detection (up to 2 hands)
-Finger-based key selection and typing
-On-screen virtual keyboard with dynamic feedback
-Auto-suggestions for word completion
-Scroll and Enter gesture recognition
-Feedback logging for gesture triggers

---

Installation

1. Clone the repository

```bash
git clone https://github.com/chaitanya-dasari/Virtual-Keyboard.git
cd Virtual-Keyboard
```
2. Setting up virtual environment
```bash
python -m venv .venv
# On Windows
.\.venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
Finally u can run your file with 
```bash
python Virtual_Keyboard.py
```