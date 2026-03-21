# Smart Election Voting System 🔗

A Face Recognition based Online Voting Application built with Flask.

## 🌟 Features

- **Face Verification** - Secure face recognition for voter authentication
- **Online Voting** - Cast your vote from anywhere
- **Live Results** - View real-time voting results
- **Profile Management** - Manage your voter profile
- **Modern UI** - Beautiful, transparent glassmorphism design

## 🚀 Quick Start

### Option 1: Single Click Run (Windows)
Simply double-click `run_app.bat` and open your browser to `http://127.0.0.1:5000`

### Option 2: Manual Setup

```bash
# Clone or download this project

# Install dependencies
pip install -r requirments.txt

# Run the application
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## 📱 Application Flow

1. **Splash Screen** - Loading page with logo
2. **Home Page** - Welcome screen with Sign Up / Login options
3. **Registration** - Create your voter account
4. **Profile Photo** - Capture your face for verification
5. **Login** - Enter your credentials
6. **Dashboard** - Access voting features
7. **Face Verification** - Verify your identity before voting
8. **Vote** - Cast your vote for your preferred candidate
9. **Results** - View live voting results

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Face Recognition:** OpenCV, scikit-learn

## 📁 Project Structure

```
Smart_Election_Voting_Using_Faace_Recognization/
├── app.py                 # Main Flask application
├── add_faces.py          # Face data collection
├── give_vote.py          # Vote processing
├── voting.db             # SQLite database
├── requirments.txt       # Python dependencies
├── run_app.bat          # One-click run script
├── static/
│   ├── css/style.css    # Stylesheets
│   ├── data/            # User face data
│   └── images/          # Static images
└── templates/            # HTML templates
    ├── splash.html
    ├── home.html
    ├── signup.html
    ├── login.html
    ├── dashboard.html
    ├── face_verify.html
    ├── vote.html
    ├── profile.html
    ├── results.html
    └── ...
```

## 🔒 Security Features

- Password hashing (SHA256)
- Session-based authentication
- Face verification before voting
- One vote per user

## 📋 Requirements

- Python 3.7+
- Webcam for face verification
- Modern web browser

## 🚀 Running Online

To share via a public link, you can use ngrok:

```bash
# Install ngrok
pip install pyngrok

# Add to app.py
from pyngrok import ngrok
public_url = ngrok.connect(5000)
print(f"Public URL: {public_url}")
```

## 📄 License

This project is for educational purposes.

---

**Note:** This is a demonstration application. For production voting systems, additional security measures and compliance with election laws would be required.
