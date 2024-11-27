from django.contrib import admin
from .models import Appointment, Request, ConsultationRequest


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'status')


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'created_at', 'status')


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'appointment_date', 'appointment_time', 'status')





