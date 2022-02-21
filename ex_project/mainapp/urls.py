from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView, UploadExcelAPIUView

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('auth/register/', RegistrationAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
    path('excel_files/', UploadExcelAPIUView.as_view()),
]