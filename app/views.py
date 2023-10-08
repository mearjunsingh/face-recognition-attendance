from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render

from algorithm.management.commands.train import train_images
from algorithm.register import take_images
from algorithm.record import track_images
from app.forms import LogForm
from app.models import Student, Attendance


def index(request):
    return render(request, "index.html")


@login_required(login_url="/admin/login/")
def register_student(request):
    serial_number = request.GET.get("serial_number")
    name = request.GET.get("name")
    msg = "Stand in front of camera till camera is closed automatically."

    if serial_number and name:
        if Student.objects.filter(serial_number=serial_number).exists():
            msg = "Student with given serial number already exists."
        else:
            take_images(serial_number, name)
            msg = "Photo Saved Successfully. Train data manually or click on train button."

    return render(request, "register.html", {"msg": msg})


@login_required(login_url="/admin/login/")
def train_face_data(request):
    train_images()
    return render(request, "register.html", {"msg": "Face data trained successfully."})


def record_attendance(request):
    try:
        track_images()
        msg = "Attendance recorded successfully!"
    except Student.DoesNotExist:
        msg = "Student does not exist."
    return render(request, "attendance.html", {"msg": msg})


def attendance_logs(request):
    form = LogForm(request.GET or None)
    if form.is_valid():
        logs = Attendance.objects.filter(
            student__serial_number=form.cleaned_data.get("serial_number"),
        ).values(
            timestamp=F("date_time"),
        )
        return render(
            request,
            "logs.html",
            {
                "logs": logs,
                "form": form,
                "name": form.cleaned_data.get("name"),
                "show_table": True,
            },
        )
    return render(request, "logs.html", {"form": form})
