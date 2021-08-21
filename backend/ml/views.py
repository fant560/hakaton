from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ml.models import Document
from ml.storage import write
from .renderers import UserJSONRenderer
from .models import AudioRecord
from .serializers import (
    RegistrationSerializer, LoginSerializer, UserSerializer
)
from datetime import datetime
import hashlib


class DocumentListView(APIView):
    # permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def get(self, request):
        document_list = Document.objects.order_by('-id')[:50]
        return JsonResponse({'documents': list(map(lambda document: {
            "id": document.id,
            "title": document.title,
            "state": document.state,
            "date_of_creation": self.get_ordinal_with_zero(document.date_of_creation.day) + '.' +
                                self.get_ordinal_with_zero(document.date_of_creation.month) + '.' +
                                str(document.date_of_creation.year)
        }, document_list))
                             })

    def get_ordinal_with_zero(self, value):
        if (value) < 10:
            return '0' + str(value)
        else:
            return str(value)


class DocumentUploadView(APIView):
    # permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def document_upload(self, request):
        if request.method == 'POST':
            for_pdf = request.POST['document_format'] == 'on'
            if for_pdf is True:
                document_format = "pdf"
            else:
                document_format = "word"
            write(request.FILES['document_file'], False, request.POST['title'], document_format, datetime.now())
            response = JsonResponse({'response': 'Document was uploaded'}, status=200)
        else:
            response = JsonResponse({'response': 'expected POST'}, status=400)
        return response


class RecordUploadView(APIView):
    # TODO раскомментировать
    # permission_classes = (IsAuthenticated,)
    extensions = ['mp3', 'mp4', 'ogg', 'wav']

    @csrf_exempt
    def post(self, request):
        if request.method == 'POST':
            # TODO валидация по типу формата файла
            title = request.data['filename']
            date_of_recording = request.data['dateOfRecording']
            try:
                if len(request.FILES.keys()) == 0:
                    return JsonResponse({
                        'response': 'Не было передано файлов!'
                    }, status=400)
                if len(request.FILES.keys()) != 1:
                    return JsonResponse({
                        'response': 'Ожидался ровно 1 файл'
                    }, status=400)
                for key in request.FILES.keys():
                    file = request.FILES[key]
                    extension = file.name.split('.')[-1]
                    if extension not in self.extensions:
                        return JsonResponse({'response': 'Неправильный формат файла, ожидался mp3/ogg/mp4/wav'},
                                            status=400)
                    key = write(request.FILES[key], True, title, extension, date_of_recording)
                    try:
                        AudioRecord.save(AudioRecord(mime_type='application/' + extension,
                                                     date_of_recording=date_of_recording,
                                                     date_of_upload=datetime.now(),
                                                     date_of_recording_end=datetime.now(),
                                                     state='Обрабатывается',
                                                     md5=hashlib.md5(key),
                                                     storage_link=key))
                    except Exception as e:
                        print(str(e))
                        return JsonResponse(
                            {'response': 'Не удалось сохранить аудиозапись, данная аудиозапись уже была загружена'},
                            status=400)
                return JsonResponse({'response': 'Аудиозапись загружена'}, status=200)
            except Exception as e:
                print("Ошибка при загрузке файла - %s" % str(e))
                return JsonResponse({'response': 'Ошибка при загрузке документа'}, status=500)
        return JsonResponse({'response': 'Ожидался POST запрос'}, status=400)


class DocumentDetailsView(APIView):
    # permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def get(self, request, document_id):
        document = get_object_or_404(Document, pk=document_id)
        return JsonResponse({'document': document})


class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям доступ к данному эндпоинту
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    @csrf_exempt
    def post(self, request):
        user = request.data.get('user', {})
        print('calling registration ' + str(user))
        # Паттерн создания сериализатора, валидации и сохранения
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = serializer.data
        print(str(response))
        return Response(response, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    @csrf_exempt
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        serializer = self.serializer_class(data={
            'username': username,
            'password': password
        })
        serializer.is_valid(raise_exception=True)

        return JsonResponse({
            'userId': serializer.validated_data['userId'],
            'username': serializer.validated_data['username'],
            'token': serializer.validated_data['token']
        })


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    @csrf_exempt
    def retrieve(self, request, *args, **kwargs):
        # Здесь нечего валидировать или сохранять. Мы просто хотим, чтобы
        # сериализатор обрабатывал преобразования объекта User во что-то, что
        # можно привести к json и вернуть клиенту.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @csrf_exempt
    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Паттерн сериализации, валидирования и сохранения - то, о чем говорили
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
