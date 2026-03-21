import cv2

def recognize_face():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return None

    print("Press 's' to simulate successful face recognition")

    name = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Face Scan - Press S to Continue", frame)

        key = cv2.waitKey(1)

        # Press S to simulate recognition
        if key == ord('s'):
            name = "demo_user"
            break

        # Press Q to quit
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return name