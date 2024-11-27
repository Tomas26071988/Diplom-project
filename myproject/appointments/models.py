
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)

class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Запланирована'),
        ('canceled', 'Отменена'),
        ('completed', 'Завершена')
    ])

class Request(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('new', 'Новая'),
        ('in_progress', 'В обработке'),
        ('closed', 'Закрыта')
    ])

User = get_user_model()

class ConsultationRequest(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20, default='pending')  # статус
    created_at = models.DateTimeField(auto_now_add=True)
    appointment_date = models.DateField()  # Поле для даты
    appointment_time = models.TimeField()  # Поле для времени

    def __str__(self):
        return f'Request by {self.user.email} - Status: {self.status}'


class Event(models.Model):
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title
    

# Create your models here.
