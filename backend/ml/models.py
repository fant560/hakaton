from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.contrib.auth.models import User


class AudioRecord(models.Model):
    # md5 сумма от целого файла, проверка уникальности(что файл нельзя загрузить дважды)
    md5 = models.CharField(max_length=60, unique=True, null=False)
    mime_type = models.CharField(max_length=40)
    date_of_upload = models.DateTimeField()
    date_of_recording = models.DateTimeField()
    date_of_recording_end = models.DateTimeField()
    state = models.CharField(max_length=20)
    # ссылка на файл в хранилище
    storage_link = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    title = models.CharField(max_length=200)
    hash = models.CharField(max_length=400, default="")


class Document(models.Model):
    # уникальный идентификатор документа в системе
    uuid = models.CharField(max_length=40, unique=True, null=False)
    audio_record_id = models.ForeignKey(AudioRecord, null=True, on_delete=models.SET_NULL)
    date_of_recording = models.DateTimeField()
    date_of_creation = models.DateTimeField()
    storage_link = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    title = models.CharField(max_length=250, null=False, default="")
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    hash = models.CharField(max_length=400, default="")


class UserDocumentReadState(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE, null=False)
    state = models.CharField(max_length=20)


class UserRole(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    role_name = models.CharField(max_length=250)
    added = models.DateTimeField()


class RoleCanViewDocument(models.Model):
    role = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    can_view = models.BooleanField(default=False)