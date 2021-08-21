import datetime
import tempfile
import os
from pathlib import Path
from dateutil.parser import parse

# $HOME (корневая папка с файлами, TODO мб вынести в настройки вообще)
user_home = Path.home()
app_base_dir = user_home.joinpath('ml')
audio_dir = app_base_dir.joinpath('audio')
document_dir = app_base_dir.joinpath('documents')

try:
    testfile = tempfile.TemporaryFile(dir=user_home)
    testfile.close()
except OSError as e:
    raise Exception("Can't write into dir " + str(user_home))
if not document_dir.exists():
    document_dir.mkdir()
if not audio_dir.exists():
    audio_dir.mkdir()


def write(file_to_store, is_audio, title, convert_format, record_date):
    if str(convert_format).startswith('.') is False:
        convert_format = '.' + convert_format
    if is_audio:
        # TODO если формат .mp4 выдернуть звук и писать только звук
        path = audio_dir
        file_name = title + convert_format
    else:
        path = document_dir
        file_name = title + convert_format
    date = parse(record_date)
    filepath = path.joinpath(str(date.year) + '-' + str(date.month) + '-' + str(date.day))
    if filepath.exists():
        filepath = filepath.joinpath(file_name)
        if filepath.exists():
            os.remove(filepath)
    else:
        os.mkdir(filepath)
        filepath = filepath.joinpath(file_name)
    with open(filepath, 'wb+') as file:
        for chunk in file_to_store.chunks():
            file.write(chunk)
    return path.joinpath(file_name).relative_to(user_home)


def read(self, file_name):
    with open(self.user_home.joinpath(file_name), 'r') as file:
        return file.read()


# TODO нужно ли удаление?
def delete(self):
    pass
