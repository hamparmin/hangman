# hangman-server

Hangman REST API written in python using flask

## Getting started

Make sure you're using python 3.8

Setup virtual env

```
virtualenv --python=python3 venv
source venv/bin/activate
```

Install requirements

```
pip install -r requirements.txt
```

Run the tests

```
python -m unittest discover tests -v
```

Start server

```
python server.py
```

Hit the API

```
POST http://localhost:5000/api/hangman
GET http://localhost:5000/api/hangman/{game_id}
```
