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
