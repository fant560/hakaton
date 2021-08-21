from rest_framework import serializers

from .models import User
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализация регистрации пользователя и создания нового
    """
    # убедитесь что пароль содержит не менее 8 символов, не более 128
    # и так же что он не может быть прочитан клиентской стороной
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # Клиентская сторона не должна иметь возможность отправлять токен вместе с запросом на регистрацию
    # Сделаем его доступным только на чтение
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # Перечислить все поля которые могут быть включены в запрос или ответ,
        # включая поля, указанные выше
        fields = ['username', 'password', 'token', 'email']

    def create(self, validated_data):
        # Использовать метод create_user, который мы написали ранее, для создания пользователя
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        print('Try to find user with username ' + data.get('username'))
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'Имя пользователя должно быть указано!'
            )

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Пользователь не найден!'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

            # Метод validate должен возвращать словать проверенных данных. Это
            # данные, которые передются в т.ч. в методы create и update.
        return {
            'userId': user.id,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов User. """

    # Пароль должен содержать от 8 до 128 символов. Это стандартное правило. Мы
    # могли бы переопределить это по-своему, но это создаст лишнюю работу для
    # нас, не добавляя реальных преимуществ, потому оставим все как есть.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'token',)

        # Параметр read_only_fields является альтернативой явному указанию поля
        # с помощью read_only = True, как мы это делали для пароля выше.
        # Причина, по которой мы хотим использовать здесь 'read_only_fields'
        # состоит в том, что нам не нужно ничего указывать о поле. В поле
        # пароля требуются свойства min_length и max_length,
        # но это не относится к полю токена.
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """ Выполняет обновление User. """

        # В отличие от других полей, пароли не следует обрабатывать с помощью
        # setattr. Django предоставляет функцию, которая обрабатывает пароли
        # хешированием и 'солением'. Это означает, что нам нужно удалить поле
        # пароля из словаря 'validated_data' перед его использованием далее.
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            # Для ключей, оставшихся в validated_data мы устанавливаем значения
            # в текущий экземпляр User по одному.
            setattr(instance, key, value)

        if password is not None:
            # 'set_password()' решает все вопросы, связанные с безопасностью
            # при обновлении пароля, потому нам не нужно беспокоиться об этом.
            instance.set_password(password)

        # После того, как все было обновлено, мы должны сохранить наш экземпляр
        # User. Стоит отметить, что set_password() не сохраняет модель.
        instance.save()

        return instance
