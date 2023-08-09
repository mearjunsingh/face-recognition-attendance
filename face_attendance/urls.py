from django.contrib import admin
from django.urls import path

from app.views import register_student, record_attendance, index, train_face_data

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register_student),
    path("record/", record_attendance),
    path("train/", train_face_data),
    path("", index),
]
