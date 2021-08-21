from django.urls import path

from .views import *

app_name = 'ml'
urlpatterns = [
    path('documents', DocumentListView.as_view()),
    path('', DocumentListView.as_view()),
    path('document/<int:document_id>', DocumentDetailsView.as_view()),
    path('document/upload', DocumentUploadView.as_view()),
    path('record/upload', RecordUploadView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('register', RegistrationAPIView.as_view()),
    path('user', UserRetrieveUpdateAPIView.as_view())
]
