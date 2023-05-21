## Task 2

### Deployment.

```
git clone git@github.com:12masek34/bewise_test_2.git

cd bewise_test_2/

docker-compose up --build
```

OpenAPI Specification ```http://0.0.0.0:8000/docs#```



##### Example:

Create user

```
curl -X 'POST' \
  'http://0.0.0.0:8000/user' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "new name"
}'
```

Add .wav file

```
curl -X 'POST' \
  'http://0.0.0.0:8000/record?id=7&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NywibmFtZSI6InRlc3RfbmFtZSJ9.5QSSL97PEOhSe0a5mWrFp_edSrB4u5T9l72GmAViL9o' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@file_example_WAV_10MG.wav;type=audio/wav'
```

Get .mp3 file

```
curl -X 'GET' \
  'http://0.0.0.0:8000/record?id=bad0a558-d764-4446-b95d-f8a7395afa46&user=7' \
  -H 'accept: */*'
```



#### Реализовать веб-сервис со следующими REST методами:

* Создание пользователя, POST:
  * Принимает на вход запросы с именем пользователя.
  
    Создаёт в базе данных пользователя заданным именем, так же генерирует уникальный идентификатор пользователя и UUID токен доступа (в виде строки) для данного пользователя.
    Возвращает сгенерированные идентификатор пользователя и токен.
  * Добавление аудиозаписи, POST:
  
    Принимает на вход запросы, содержащие уникальный идентификатор пользователя, токен доступа и аудиозапись в формате wav.
    Преобразует аудиозапись в формат mp3, генерирует для неё уникальный UUID идентификатор и сохраняет их в базе данных.
    Возвращает URL для скачивания записи вида http://host:port/record?id=id_записи&user=id_пользователя.
  * Доступ к аудиозаписи, GET:
  
    Предоставляет возможность скачать аудиозапись по ссылке из передидущего пункта.
