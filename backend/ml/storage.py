import os
import tempfile
from pathlib import Path
import hashlib

from dateutil.parser import parse

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
        path = audio_dir
        file_name = title + convert_format
    else:
        path = document_dir
        file_name = title + convert_format
    if isinstance(record_date, str):
        date = parse(record_date)
    else:
        date = record_date
    filepath = path.joinpath(str(date.year) + '-' + str(date.month) + '-' + str(date.day))
    file_name = hashlib.sha1(file_name.encode()).hexdigest() + convert_format
    if filepath.exists():
        filepath = filepath.joinpath(file_name)
        if filepath.exists():
            os.remove(filepath)
    else:
        os.mkdir(filepath)
        filepath = filepath.joinpath(file_name)
    if isinstance(file_to_store, str):
        bytesA = bytes(file_to_store, encoding='utf8')
    else:
        bytesA = file_to_store.read()
    with open(filepath, 'wb+') as file:
        file.write(bytesA)
    return filepath, file_name


def read(self, file_name):
    with open(self.user_home.joinpath(file_name), 'r') as file:
        return file.read()
