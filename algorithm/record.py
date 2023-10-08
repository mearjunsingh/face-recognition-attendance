import cv2

from django.conf import settings

from app.models import Attendance, Student


def track_images():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(str(settings.TRAINER_FILE))
    face_cascade = cv2.CascadeClassifier(str(settings.HAARCASCADE_FILE))

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        _, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)
        for x, y, w, h in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            serial_number, conf = recognizer.predict(gray[y : y + h, x : x + w])  # noqa
            if conf < 50:
                student = Student.objects.get(serial_number=serial_number)
                name = student.name
            else:
                continue

            cv2.putText(im, name, (x, y + h), font, 1, (0, 251, 255), 2)  # noqa

        cv2.imshow("Taking Attendance", im)
        if cv2.waitKey(1) == ord("q"):  # cv2.waitKey(3000)
            break

    Attendance.new(serial_number=serial_number)
    cam.release()
    cv2.destroyAllWindows()
