from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=100)
    date_or_recording = forms.DateField()
    file = forms.FileField()
