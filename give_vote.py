import cv2
import pickle
import numpy as np
import sqlite3
import os

MODEL_PATH = "model/face_model.pkl"
FACE_SIZE = (100, 100)

# ----------------------------
# DATABASE SETUP
# ----------------------------
def init_db():
    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            has_voted INTEGER DEFAULT 0,
            vote_to TEXT
        )
    """)

    conn.commit()
    conn.close()


# ----------------------------
# CHECK & UPDATE VOTE
# ----------------------------
def process_vote(voter_name):
    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()

    cursor.execute("SELECT has_voted FROM voters WHERE name=?", (voter_name,))
    result = cursor.fetchone()

    if result is None:
        cursor.execute("INSERT INTO voters (name, has_voted) VALUES (?, 0)", (voter_name,))
        conn.commit()
        has_voted = 0
    else:
        has_voted = result[0]

    if has_voted == 1:
        print("❌ You have already voted.")
        conn.close()
        return

    print("\nCandidates:")
    print("1. Candidate_A")
    print("2. Candidate_B")

    choice = input("Enter your vote (1/2): ")

    if choice == "1":
        candidate = "Candidate_A"
    elif choice == "2":
        candidate = "Candidate_B"
    else:
        print("Invalid choice.")
        conn.close()
        return

    cursor.execute("""
        UPDATE voters
        SET has_voted=1, vote_to=?
        WHERE name=?
    """, (candidate, voter_name))

    conn.commit()
    conn.close()

    print("✅ Vote recorded successfully!")


# ----------------------------
# FACE RECOGNITION + VOTING
# ----------------------------
def recognize_and_vote():
    if not os.path.exists(MODEL_PATH):
        print("Train model first!")
        return

    with open(MODEL_PATH, "rb") as f:
        model_data = pickle.load(f)

    faces = model_data["faces"]
    labels = model_data["labels"]
    label_map = model_data["label_map"]

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(0)
    print("Scanning face...")

    recognized_name = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected_faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in detected_faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, FACE_SIZE).flatten()

            distances = np.linalg.norm(faces - face, axis=1)
            min_index = np.argmin(distances)

            predicted_label = labels[min_index]
            name = label_map[predicted_label]

            recognized_name = name

            cv2.putText(frame, name, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0,255,0), 2)

            cv2.rectangle(frame, (x, y), (x+w, y+h),
                          (0,255,0), 2)

        cv2.imshow("Smart Voting - Face Scan", frame)

        if cv2.waitKey(1) == 27 or recognized_name is not None:
            break

    cap.release()
    cv2.destroyAllWindows()

    if recognized_name:
        print(f"Recognized as: {recognized_name}")
        process_vote(recognized_name)
    else:
        print("Face not recognized.")


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    init_db()
    recognize_and_vote()