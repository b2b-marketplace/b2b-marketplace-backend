# backend

## Схема базы данных
Обновление картинки после изменения dbml с помощью команды:
```
npx --package=@softwaretechnik/dbml-renderer -- dbml-renderer -i docs/db.dbml -o docs/db.svg
```

Схему БД в интерактивном режиме можно посмотреть по ссылке:

[СХЕМА БД](https://dbdiagram.io/d/64bb081202bd1c4a5e7f8c0b)



## Документация API
В проекте реализована автоматическая генерация документации. Документация доступна по адресам:
1) Swagger: `/api/v1/schema/swagger-ui/`
2) Redoc: `/api/v1/schema/redoc/`



## Запуск в режиме разработки

1. Убедитесь, что у вас установлены Docker и Docker Compose.

2. Склонируйте данный репозиторий на свой локальный компьютер:

   ```bash
   git clone https://github.com/b2b-marketplace/b2b-marketplace-backend.git
   ```

3. Перейдите в директорию с проектом:

   ```bash
   cd b2b-marketplace-backend
   ```

4. Создайте файл .env внутри директории infra с переменными окружения
   и скопируйте в него данные из файла ".env.example":

   ```bash
   touch infra/.env
   ```
   В приведенном примере .env файла:

   ```bash
         # Параметры Django
         DJANGO_SUPERUSER_PASSWORD # Пароль для суперпользователя Django, который будет создан при инициализации приложения.
         DJANGO_SECRET_KEY # Секретный ключ Django, используемый для хэширования паролей, создания токенов и других целей безопасности.
         DJANGO_ALLOWED_HOSTS # Список разрешенных хостов, которые могут обращаться к вашему Django-приложению.
         CSRF_TRUSTED_ORIGINS # Список доверенных источников, которым разрешается отправлять запросы с токенами CSRF.
         DJANGO_DEBUG # Указывает, включен ли режим отладки в Django. Должен быть выключен в рабочем окружении.

         # Параметры для подключения к базе данных PostgreSQL.
         POSTGRES_DB # имя БД
         POSTGRES_USER # имя пользователя БД
         POSTGRES_PASSWORD # пароль пользователя БД
         POSTGRES_HOST # хост, на котором развернута БД
         POSTGRES_PORT # порт, на котором развернута БД

         # Параметры для подключения к тестовой базе данных PostgreSQL.
         POSTGRES_DB_TEST # имя тестовой БД
         POSTGRES_USER_TEST # имя пользователя тестовой БД
         POSTGRES_PASSWORD_TEST # пароль пользователя тестовой БД
         POSTGRES_HOST_TEST # хост, на котором развернута тестовая БД
         POSTGRES_PORT_TEST  # порт, на котором развернута тестовая БД

         # Параметры почтового ящика, для исходящей почты
         EMAIL_HOST # имя хоста (например, smpt.mail.ru)
         EMAIL_PORT # порт хоста электронной почты
         EMAIL_HOST_USER # имя пользователя (адрес электронный почты)
         EMAIL_HOST_PASSWORD # пароль электронной почты
      ```

5. Соберите Docker-образы и запустите контейнеры:

   ```bash
   docker-compose -f infra/docker-compose.dev.yml build
   ```

   ```bash
   docker-compose -f infra/docker-compose.dev.yml up -d
   ```
6. После успешного запуска, Django приложение будет
доступно по адресу http://localhost:8000/.

7. Теперь вы можете войти в административную панель Django
по адресу http://localhost:8000/admin/,
используя созданные учетные данные:
   ```
   username: admin
   пароль: mysecretpassword
   ```
8. Вы можете остановить контейнеры с помощью команды:

   ```bash
   docker-compose -f infra/docker-compose.dev.yml down
   ```

## Пакетное обновление цен

В приложение добавлена возможность обновить цены товаров из файла.

Для этого необходимо:
1. Выгрузить из 1С или другой программы CSV файл с новыми ценами.

   Файл должен состоять из двух полей с заголовками "sku" и "price".

   Пример:

         sku,price
         sku1,10.99
         sku2,25.50
         sku3,5.75
   Где "sku" - это уникальный артикул товара, а "price" - новая цена.

2. Загрузить csv-файл на сервер в директорию с проектом.

3. _Использование:_
   ```sh
   python manage.py update_prices --username <username> --file_path <file_path>
   ```
   _Аргументы:_

   -  **--username**: Имя пользователя, чьи цены на товары нужно обновить.

   -  **--file_path**: Путь к CSV-файлу с обновленными ценами.

4. _Пример:_
   ```shell
   python manage.py update_prices --username user1 --file_path /путь/к/файлу/с/ценами.csv
   ```
