from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app.views import register_student, record_attendance, index, train_face_data, attendance_logs

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register_student),
    path("record/", record_attendance),
    path("train/", train_face_data),
    path("logs/", attendance_logs),
    path("", index),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
