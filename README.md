# Hotzone

A Django Web Application using DBScan algorithm to perform clustering of COVID-19 cases in Hong Kong 

### Deployed at

https://hotzoneteamg.herokuapp.com

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
