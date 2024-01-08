import cv2

max_capture_count = 10

cap = cv2.VideoCapture(0)  # 카메라 번호 (0: 기본 카메라)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

capture_count = 0

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(200, 200))
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        capture_count += 1
        face_image = img[y:y + h, x:x + w]
        cv2.imwrite("face"+str(capture_count)+".jpg", face_image)
    cv2.imshow("cam",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if capture_count >= max_capture_count:
        break

cap.release()
cv2.destroyAllWindows()
