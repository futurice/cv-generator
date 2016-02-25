# Futurice CV Generator

## Running locally

To run, you need Python 3 and Redis. In a Python virtualenv do

```
$ pip install -r requirements.txt
$ npm install
$ npm run build-js
$ npm run build-sass
$ python main.py
```

And open http://localhost:8080 in a browser

## Running in Docker

To run in Docker, place the required font files in the `fonts` directory and run

```
$ docker-compose up
```

Then check the output of `docker-compose port futucv 8080` to see what external port was allocated.
