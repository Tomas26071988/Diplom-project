# appointments/urls.py
from django.urls import path, include
from .views import register, login_view, logout_view, dashboard, new_request_view, my_requests_view, MyRequestsAPI
from rest_framework.routers import DefaultRouter
from .views import EventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('new_request/', new_request_view, name='new_request'),
    path('my_requests/', my_requests_view, name='my_requests'),
    path('api/', include(router.urls)),
    path('api/my_requests/', MyRequestsAPI.as_view(), name='my_requests_api'),
    path('api/my_requests/<int:pk>/', MyRequestsAPI.as_view(), name='my_requests_api_update'),
]
