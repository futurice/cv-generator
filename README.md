# Futurice CV Generator

Note, you need to add copies of some Sharp Sans fonts under `fonts/` to use with Docker or have them installed in your system font storage for usage locally.

## Running locally

To run, you need Python 3 and Postgresql. In a Python virtualenv do

```
$ pip install -r requirements.txt
$ npm install
$ npm run build-js
$ npm run build-sass
$ python main.py
```

And open http://localhost:8080 in a browser

## Running in Docker

To run in Docker, install Docker with Docker Compose and run

```
$ docker-compose up
```

Then check the output of `docker-compose port futucv 8080` to see what external port was allocated.
