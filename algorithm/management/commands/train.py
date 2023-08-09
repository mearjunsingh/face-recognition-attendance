import os

import cv2
import numpy as np
from PIL import Image

from django.conf import settings
from django.core.management.base import BaseCommand


def get_image_and_labels(images_dir: str):
    image_paths = [os.path.join(images_dir, f) for f in os.listdir(images_dir)]

    faces, serial_numbers = [], []
    for image_path in image_paths:
        pillow_image = Image.open(image_path).convert("L")
        numpy_image = np.array(pillow_image, "uint8")
        serial_number = int(str(image_path).split(".")[-3])
        faces.append(numpy_image)
        serial_numbers.append(serial_number)

    return faces, serial_numbers


def train_images():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    faces, ID = get_image_and_labels(str(settings.TRAINING_IMAGES_DIR))
    recognizer.train(faces, np.array(ID))
    recognizer.save(str(settings.TRAINER_FILE))


class Command(BaseCommand):
    help = "Train Model with new Images"

    def handle(self, *args, **options):
        train_images()
