import cv2

from django.conf import settings

from app.models import Student


def take_images(serial_number: int, name: str):
    cam = cv2.VideoCapture(0)

    detector = cv2.CascadeClassifier(str(settings.HAARCASCADE_FILE))

    sample_count = 0
    while True:
        _, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.05, 5)

        for x, y, w, h in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            sample_count += 1
            image_filename = f"{name}.{serial_number}.{sample_count}.jpg"
            image_filepath = settings.TRAINING_IMAGES_DIR / image_filename

            cv2.imwrite(str(image_filepath), gray[y : y + h, x : x + w])  # noqa
            cv2.imshow("Taking Images", img)

        if (cv2.waitKey(100) & 0xFF == ord("q")) or (sample_count > 100):
            break

    cam.release()
    cv2.destroyAllWindows()

    return Student.objects.create(name=name, serial_number=serial_number)
