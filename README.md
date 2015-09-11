# README #

### Что это за фигня? ###
Сайт ФИВТ, со стиралкой и системой активистов

### Как запустить эту фигню? ###

* Pre-requirements: Python 3.4+
* Нужно любым образом скачать последнюю рабочую версию из deploy ветки (лучше всего это делается с git clone)
* Поставить все пакеты из requirements. Проще всего через pip. Если не получается, попробуй в virtualenv или с правами суперпользователя:

```
#!bash

pip3 install -r <path-to-requirements.txt>
```

* Dev-сервер (всё выполняется в папке с manage.py):

```
#!bash
mkdir db
python3 manage.py migrate
python3 manage.py thumbnail cleanup
python3 manage.py create_groups
python3 manage.py create_sectors
python3 manage.py create_superuser --username <username> --password <password>
python3 manage.py runserver <ip:port>
```

* Deploy-сервер лучше всего поднимать через Docker с уже настроенными конфигами. Брать их нужно у того, кто ими пользуется сейчас, здесь их можешь не искать. Если коротко, нужно прописать почтовый сервер, настроить social_auth, ALLOWED_HOSTS, DEBUG=False, поднять nginx с uwsgi. Если ты не понял, что вообще в предыдущем предложении написано, специально для тебя есть deploy-bot: https://diht.deploybot.com/

* Тесты очень легко запускаются.

```
#!bash

python3 manage.py test
```

* Но если ты опять ленивая задница, все тесты автоматически прогоняются при любом коммите на https://codeship.com/

### Как поучаствовать в развитии этой фигни? ###

* В deploy ветку нельзя пушить. Совсем. Только pull requests, только хардкор! Пилишь всё в своей отдельной ветке и потом делаешь pull request. На него делают review и, возможно, пускают в deploy.
* Issue tracker: https://bitbucket.org/phoenix120/2ka/issues
* Тесты нужны. Серьёзно. Лучше пиши их сразу.
* Что тебе нужно сделать, чтобы поменять структуру базы на deploy-сервере:

```
#!python

python3 manage.py makemigrations <app_name>
```


### У кого можно спрашивать по поводу этой фигни? ###

* Пиши Илье Гусеву. Если он не отвечает, Денису Шапошникову.