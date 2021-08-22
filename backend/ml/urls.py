from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

app_name = 'ml'
urlpatterns = [
    path('documents', DocumentListView.as_view()),
    path('', DocumentListView.as_view()),
    path('document/<int:document_id>', DocumentDetailsView.as_view()),
    path('record/upload', RecordUploadView.as_view()),
    path('register', RegistrationAPIView.as_view()),
    path('user', UserRetrieveUpdateAPIView.as_view()),
    path('token-refresh', TokenRefreshView.as_view(), name="token_refresh"),
    path('login', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('document/download/<int:document_id>', DownloadDocumentView.as_view())
]
