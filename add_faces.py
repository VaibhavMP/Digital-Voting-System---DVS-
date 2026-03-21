import cv2
import pickle
import numpy as np
import os

# ---------------------------
# CONFIG
# ---------------------------
DATA_PATH = "data"
MODEL_PATH = "model/face_model.pkl"
FACE_SIZE = (100, 100)

# Create directories if not exist
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs("model", exist_ok=True)

# ---------------------------
# FACE DETECTOR
# ---------------------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ---------------------------
# REGISTER NEW USER
# ---------------------------
def register_user(user_id):
    user_path = os.path.join(DATA_PATH, user_id)
    os.makedirs(user_path, exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0

    print("Collecting face data... Look at camera.")

    while count < 50:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, FACE_SIZE)

            file_name = os.path.join(user_path, f"{count}.jpg")
            cv2.imwrite(file_name, face)

            count += 1
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        cv2.imshow("Register Face", frame)

        if cv2.waitKey(1) == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Face data collection completed.")

# ---------------------------
# TRAIN MODEL (KNN)
# ---------------------------
def train_model():
    faces = []
    labels = []
    label_map = {}
    label_id = 0

    for user in os.listdir(DATA_PATH):
        user_path = os.path.join(DATA_PATH, user)
        if not os.path.isdir(user_path):
            continue

        label_map[label_id] = user

        for img_name in os.listdir(user_path):
            img_path = os.path.join(user_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, FACE_SIZE)

            faces.append(img.flatten())
            labels.append(label_id)

        label_id += 1

    faces = np.array(faces)
    labels = np.array(labels)

    model_data = {
        "faces": faces,
        "labels": labels,
        "label_map": label_map
    }

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model_data, f)

    print("Model trained and saved.")

# ---------------------------
# RECOGNIZE FACE
# ---------------------------
def recognize_face():
    if not os.path.exists(MODEL_PATH):
        print("Train model first!")
        return

    with open(MODEL_PATH, "rb") as f:
        model_data = pickle.load(f)

    faces = model_data["faces"]
    labels = model_data["labels"]
    label_map = model_data["label_map"]

    cap = cv2.VideoCapture(0)

    print("Starting recognition...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected_faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in detected_faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, FACE_SIZE).flatten()

            # Simple KNN (Euclidean distance)
            distances = np.linalg.norm(faces - face, axis=1)
            min_index = np.argmin(distances)

            predicted_label = labels[min_index]
            name = label_map[predicted_label]

            cv2.putText(frame, name, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0,255,0), 2)

            cv2.rectangle(frame, (x, y), (x+w, y+h),
                          (0,255,0), 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# ---------------------------
# MAIN MENU
# ---------------------------
if __name__ == "__main__":
    print("1. Register User")
    print("2. Train Model")
    print("3. Recognize Face")

    choice = input("Enter choice: ")

    if choice == "1":
        user_id = input("Enter User ID: ")
        register_user(user_id)
    elif choice == "2":
        train_model()
    elif choice == "3":
        recognize_face()