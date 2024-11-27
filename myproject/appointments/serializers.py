
from rest_framework import serializers
from .models import Event, ConsultationRequest  # Импортируем модель ConsultationRequest

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'  # Включаем все поля

class ConsultationRequestSerializer(serializers.ModelSerializer):  # Новый сериализатор для ConsultationRequest
    class Meta:
        model = ConsultationRequest
        fields = '__all__'  # Включаем все поля

