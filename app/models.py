from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=200)
    serial_number = models.IntegerField(unique=True, db_index=True, editable=False)

    def __str__(self):
        return f"{self.serial_number} - {self.name}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def new(cls, serial_number):
        student = Student.objects.get(serial_number=serial_number)
        return cls.objects.create(student=student)

    def __str__(self):
        return f"{self.student.serial_number} - {self.date_time}"
