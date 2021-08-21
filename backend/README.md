Сборка и запуск в первый раз:
1. Должен быть установлен docker-compose
2. sudo docker-compose build && sudo docker-compose up
3. Потом запускаем фронт и смотрим в браузер


Последующие сборки(имеет смысл только после изменений файлов бэка)
1. sudo docker-compose down
2. sudo docker-compose build --no-cache
3. sudo docker-compose up (-d чтобы не держать консоль)