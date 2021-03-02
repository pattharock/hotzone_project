# Hotzone

### Jira link

https://hotzone.atlassian.net/

### Requirements

```
- django
- requests
```

### Getting started

To create superuser:
```
python manage.py createsuperuser
```

To run development server locally:
```
python -m pipenv shell # activate virtual environment in repo root
cd hotzone
python manage.py runserver
```

To run server with <i>Waitress</i>:
```
python -m pipenv shell # activate virtual environment in repo root
cd hotzone
waitress-serve config.wsgi:application
```
