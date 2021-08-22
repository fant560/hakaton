import hashlib
import json
import os
import uuid
from datetime import datetime

import requests
from django.contrib.auth.models import Permission
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ml.storage import write
from .models import AudioRecord, Document
from .serializers import (
    RegisterSerializer, UserSerializer
)


class DocumentListView(APIView):
    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def get(self, request):
        records = AudioRecord.objects.filter(state='Обрабатывается')[:10]
        for record in records:
            data = json.loads(requests.get(f'http://ml:9090/status?file_id={record.hash}').text)
            if data is not None:
                print(data)
                status = data['status']
                if status != 'transcribing':
                    text = ''
                    for element in data['data']:
                        start_ms = element['start_ms']
                        transcription = element['transcription']
                        minutes = int(start_ms) // 60_000
                        seconds = int(start_ms) // 1000
                        if transcription.strip() == '':
                            continue
                        text += f'**{minutes}:{seconds}** {transcription}  \n'
                    if record is None:
                        raise Exception("Can't find audio record from document with title ")
                    user = record.created_by
                    if user is None:
                        raise Exception("Can't find user who created audio record")
                    record.state = 'Обработано'
                    record.save()
                    filepath, hash = write(text, False, record.hash, '.txt', record.date_of_recording)
                    Document.objects.create(uuid=uuid.uuid4(),
                                            audio_record_id=record,
                                            created_by=user,
                                            storage_link=filepath,
                                            date_of_recording=record.date_of_recording,
                                            date_of_creation=datetime.now(),
                                            title=record.title,
                                            state='Успешно обработан',
                                            hash=hash)

        perm_list = [x.name for x in Permission.objects.filter(user=request.user)]
        if perm_list.__contains__('admin'):
            document_list = Document.objects.order_by('-id')[:25]
        else:
            document_list = Document.objects.filter(created_by=request.user).order_by('-id')[:25]
        return JsonResponse({'documents': list(map(lambda document: {
            "id": document.id,
            "title": document.title,
            "state": document.state,
            "date_of_creation": self.get_ordinal_with_zero(document.date_of_creation.day) + '.' +
                                self.get_ordinal_with_zero(document.date_of_creation.month) + '.' +
                                str(document.date_of_creation.year)
        }, document_list))
                             })

    @staticmethod
    def get_ordinal_with_zero(value):
        if value < 10:
            return '0' + str(value)
        else:
            return str(value)


class DownloadDocumentView(APIView):
    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def get(self, request):
        document_id = request.path.split('/')[-1]
        file_path = Document.objects.get(pk=document_id).storage_link
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404


class RecordUploadView(APIView):
    permission_classes = (IsAuthenticated,)
    extensions = ['mp3', 'mp4', 'ogg', 'wav']

    @csrf_exempt
    def post(self, request):
        if request.method == 'POST':
            title = request.data['filename']
            date_of_recording = datetime.strptime(
                request.data['dateOfRecording'][0:request.data['dateOfRecording'].rfind(" ")],
                '%a %b %d %Y %H:%M:%S'
            )

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
                date_of_uploading_start = datetime.now()
                filepath, hash = write(request.FILES[key], True, title, extension, date_of_recording)
                with open(filepath, 'rb') as file_to_send:
                    response = requests.post('http://ml:9090/transcribe', files={
                        'file': file_to_send
                    }).text
                    data = json.loads(response)
                    file_id = data['file_id']
                AudioRecord.save(AudioRecord(mime_type='application/' + extension,
                                             date_of_recording=date_of_recording,
                                             date_of_upload=date_of_uploading_start.now(),
                                             date_of_recording_end=datetime.now(),
                                             state='Обрабатывается',
                                             md5=hashlib.md5(str(file_id).encode()).hexdigest(),
                                             storage_link=key,
                                             created_by=request.user,
                                             title=title,
                                             hash=file_id))

            return JsonResponse({'response': 'Аудиозапись загружена'}, status=200)
        return JsonResponse({'response': 'Ожидался POST запрос'}, status=400)


class DocumentDetailsView(APIView):
    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def get(self, request, document_id):
        document = get_object_or_404(Document, pk=document_id)
        if document.created_by != request.user:
            perm_tuple = [x.name for x in Permission.objects.filter(user=request.user)]
            if not perm_tuple.__contains__('admin'):
                return JsonResponse({
                    "exception": 'У пользователя нет прав на просмотр данного документа'
                }, status=400)
        return JsonResponse({
            "id": document.id,
            "title": document.title,
            "state": document.state,
            "date_of_creation": DocumentListView.get_ordinal_with_zero(document.date_of_creation.day) + '.' +
                                DocumentListView.get_ordinal_with_zero(document.date_of_creation.month) + '.' +
                                str(document.date_of_creation.year),
            "text": self.get_text(document.storage_link)
        })

    def get_text(self, link):
        file = open(link, 'r', encoding='utf-8')
        return file.read()

class RegistrationAPIView(generics.GenericAPIView):
    """
    Разрешить всем пользователям доступ к данному эндпоинту
    """
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @csrf_exempt
    def retrieve(self, request, *args, **kwargs):
        return JsonResponse({
            "id": request.user.id,
            "username": request.user.username
        }, status=status.HTTP_200_OK)
