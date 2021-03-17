from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView, UploadExcelAPIUView

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/',  RegistrationAPIView.as_view()),
    path('users/login/',  LoginAPIView.as_view()),
    path('list/',  UploadExcelAPIUView.as_view()),
]