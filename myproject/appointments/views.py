import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, status
from .forms import UserRegistrationForm, ConsultationRequestForm
from .models import ConsultationRequest, Event
from django.contrib.auth.decorators import login_required
from .utils import send_sms
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ConsultationRequestSerializer, EventSerializer

logger = logging.getLogger('myproject')  # добавляем логгирование


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            logger.info(f'Пользователь зарегистрирован: {user.email}')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'appointments/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            logger.info(f'Успешный вход: {user.email}')
            print("Успешный вход:", user.username)
            return redirect('dashboard')  # redirect к dashboard
        else:
            logger.warning(f'Неверные учетные данные для {email}')
            print("Неверные учетные данные")
            return render(request, 'appointments/login.html', {'error': "Неверные учетные данные"})

    return render(request, 'appointments/login.html')


def logout_view(request):
    logger.info(f'Пользователь {request.user.email} вышел из системы')
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    requests = ConsultationRequest.objects.filter(user=request.user)
    logger.info(f'Пользователь {request.user.email} открывает личный кабинет')
    return render(request, 'appointments/dashboard.html', {'requests': requests})


def new_request_view(request):
    if request.method == 'POST':
        form = ConsultationRequestForm(request.POST)
        if form.is_valid():
            consultation_request = form.save(commit=False)
            consultation_request.user = request.user  # связываем заявку с текущим пользователем
            messages.success(request, 'Заявка успешно создана!')
            logger.info(
                f'Заявка на консультацию создана: {consultation_request.description} пользователем {request.user.email}')

            consultation_request.save()

            # Подготовка сообщения для отправки
            message_body = f"Ваша консультация успешно запланирована. \nДетали: {consultation_request.description}."
            api_key = "ваш_ключ_API_здесь"  # Использовать потом API-ключ
            sms_result = send_sms(request.user.phone, message_body, api_key)  # Отправка SMS
            logger.debug(f'Результат отправки SMS: {sms_result}')  # логируем отправку смс
            print(sms_result)  # Печатаем результат отправки

            return redirect('my_requests')  # на страницу, где видно все заявки
        else:
            logger.error(f'Ошибка при создании заявки: {form.errors}')  # Логируем ошибки формы для отладки
            print(form.errors)  # Вывод ошибок формы для отладки
    else:
        form = ConsultationRequestForm()
    return render(request, 'appointments/new_request.html', {'form': form, 'exception_notes': form.errors})


@login_required
def my_requests_view(request):
    requests = ConsultationRequest.objects.filter(user=request.user)
    logger.info(f'Пользователь {request.user.email} просматривает свои заявки')
    return render(request, 'appointments/my_requests.html', {'requests': requests})


# API для получения, создания и обновления заявок пользователя
class MyRequestsAPI(APIView):
    permission_classes = [IsAuthenticated]  # Доступ только для аутентифицированных пользователей

    def get(self, request):
        # Получение заявок текущего пользователя
        requests = ConsultationRequest.objects.filter(user=request.user)
        serializer = ConsultationRequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Создание новой заявки
        serializer = ConsultationRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Связываем заявку с текущим пользователем
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        # Обновление существующей заявки
        try:
            consultation_request = ConsultationRequest.objects.get(pk=pk, user=request.user)
        except ConsultationRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ConsultationRequestSerializer(consultation_request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        # Частичное обновление существующей заявки
        try:
            consultation_request = ConsultationRequest.objects.get(pk=pk, user=request.user)
        except ConsultationRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ConsultationRequestSerializer(consultation_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API для работы с событиями
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
