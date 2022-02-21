import multiprocessing

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView , ListCreateAPIView
from rest_framework.exceptions import ValidationError

from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer ,ExcelSerializer
from .renderers import UserJSONRenderer, ExcelJSONRenderer
from .models import ExcelFile


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UploadExcelAPIUView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExcelSerializer
    renderer_classes = (ExcelJSONRenderer,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ex_file = serializer.save(user=request.user)
            try:
                process = multiprocessing.Process(target=ex_file.processing_file, name='Process File')
                process.start()
                process.join()
            except Exception:
                raise ValidationError('Данный файл excel не соответствует заданию')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        excel_files = ExcelFile.objects.filter(user=request.user)
        serializer = self.serializer_class(excel_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
