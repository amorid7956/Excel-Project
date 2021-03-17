from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView , ListCreateAPIView
from rest_framework.exceptions import ValidationError
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer ,ExcelSerializer
from .renderers import UserJSONRenderer, ExcelJSONRenderer
from .models import ExcelFile
import threading

class  RegistrationAPIView(APIView):

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
        return Response(serializer.data, status = status.HTTP_200_OK)

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
            obj = serializer.save(user=request.user)
            try:
                thread = threading.Thread(obj.proccessing_file())
                thread.start()
            except:
                raise ValidationError('Данный файл excel не соответствует заданию') #Если в файле нет столбцов before или after, то
                            #поднимаем исключение(Пока что только обрабатываем ValidationError, чтобы ответ с ошибкой был в формате JSON)
            print(serializer.data)  # Делаем print, что бы заняло немного времени,
            # чтобы продемонстрировать, что в ответе мы получим
            # result = 0,  но на данный момент метод обработки excel файла
            # уже обработает файл и в БД запишется нормальный результат
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        excel_files = ExcelFile.objects.filter(user=request.user)
        serializer = self.serializer_class(excel_files,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

