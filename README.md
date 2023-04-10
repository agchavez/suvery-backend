## SurveryBackend

### Configuracones ambiente de desarrollo
Instalaciones necesarias:
1. Instalar [python 3.10](https://www.python.org/downloads/release/python-3100/)
2. Instalar [pipenv](https://pypi.org/project/pipenv/)

Pasos para correr el proyecto:
1. Clonar el repositorio
2. Crear un archivo .env en la raiz del proyecto con las siguientes variables:
```
   touch .env
```
   
```
    DB_NAME=
    DB_HOST=
    DB_USER=
    DB_PASSWORD=
    DB_PORT
    # redis
    REDIS_HOST=
    REDIS_PORT=
    REDIS_PASSWORD=
 ```

3. Instalar dependencias
```
    pipenv install -r requirements.txt
```

4. Correr migraciones
```
    pipenv run python manage.py migrate
```

5. Levantar contenedores
```
    docker-compose up -d
```

6. Correr servidor
```
    pipenv run python manage.py runserver
```

