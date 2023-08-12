# backend

## Схема базы данных
Обновление картинки после изменения dbml с помощью команды:
```
npx --package=@softwaretechnik/dbml-renderer -- dbml-renderer -i docs/db.dbml -o docs/db.svg
```

Схему БД в интерактивном режиме можно посмотреть по ссылке:

[СХЕМА БД](https://dbdiagram.io/d/64bb081202bd1c4a5e7f8c0b)


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