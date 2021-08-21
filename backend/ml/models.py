import jwt
from django.db import models
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    """
        Django требует, чтобы кастомные пользователи определяли свой собственный
        класс Manager. Унаследовавшись от BaseUserManager, мы получаем много того
        же самого кода, который Django использовал для создания User (для демонстрации).
        """

    def create_user(self, username, email, password=None):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Каждому пользователю нужен понятный человеку уникальный идентификатор,
    # который мы можем использовать для предоставления User в пользовательском
    # интерфейсе. Мы так же проиндексируем этот столбец в базе данных для
    # повышения скорости поиска в дальнейшем.
    username = models.CharField(db_index=True, max_length=255, unique=True)

    # Так же мы нуждаемся в поле, с помощью которого будем иметь возможность
    # связаться с пользователем и идентифицировать его при входе в систему.
    # Поскольку адрес почты нам нужен в любом случае, мы также будем
    # использовать его для входы в систему, так как это наиболее
    # распространенная форма учетных данных на данный момент (ну еще телефон).
    email = models.EmailField(db_index=True, unique=True)

    # Когда пользователь более не желает пользоваться нашей системой, он может
    # захотеть удалить свой аккаунт. Для нас это проблема, так как собираемые
    # нами данные очень ценны, и мы не хотим их удалять :) Мы просто предложим
    # пользователям способ деактивировать учетку вместо ее полного удаления.
    # Таким образом, они не будут отображаться на сайте, но мы все еще сможем
    # далее анализировать информацию.
    is_active = models.BooleanField(default=True)

    # Этот флаг определяет, кто может войти в административную часть нашего
    # сайта. Для большинства пользователей это флаг будет ложным.
    is_staff = models.BooleanField(default=False)

    # Временная метка создания объекта.
    created_at = models.DateTimeField(auto_now_add=True)

    # Временная метка показывающая время последнего обновления объекта.
    updated_at = models.DateTimeField(auto_now=True)

    # Дополнительный поля, необходимые Django
    # при указании кастомной модели пользователя.

    # Свойство USERNAME_FIELD сообщает нам, какое поле мы будем использовать
    # для входа в систему. В данном случае мы хотим использовать почту.
    USERNAME_FIELD = 'username'
    # Сообщает Django, что определенный выше класс UserManager
    # должен управлять объектами этого типа.
    objects = UserManager()

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.email

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.username

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.username

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        print('generating token')
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%d'))
        }, settings.SECRET_KEY, algorithm='HS256')
        print(token)
        return token


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


class Document(models.Model):
    # уникальный идентификатор документа в системе
    uuid = models.CharField(max_length=40, unique=True, null=False)
    audio_record_id = models.ForeignKey(AudioRecord, null=True, on_delete=models.SET_NULL)
    date_of_recording = models.DateTimeField()
    date_of_creation = models.DateTimeField()
    storage_link = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    title = models.CharField(max_length=250, null=False, default="")


class UserDocumentReadState:
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE, null=False)
    state = models.CharField(max_length=20)
