from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from algorithm.management.commands.train import train_images
from algorithm.register import take_images
from algorithm.record import track_images
from app.models import Student


def index(request):
    return render(request, "index.html")


@login_required(login_url="/admin/login/")
def register_student(request):
    serial_number = request.GET.get("serial_number")
    name = request.GET.get("name")
    context = {"msg": "Stand in front of camera till camera is closed automatically."}

    if serial_number and name:
        if Student.objects.filter(serial_number=serial_number).exists():
            context["msg"] = "Student with given serial number already exists."
        else:
            take_images(serial_number, name)
            context[
                "msg"
            ] = "Photo Saved Successfully. Train data manually or click on train button."

    return render(request, "register.html", context)


@login_required(login_url="/admin/login/")
def train_face_data(request):
    train_images()
    return render(request, "register.html", {"msg": "Face data trained successfully."})


def record_attendance(request):
    context = {}
    try:
        track_images()
        context["msg"] = "Attendance recorded successfully!"
    except Student.DoesNotExist:
        context["msg"] = "Student does not exist."
    return render(request, "attendance.html", context)
