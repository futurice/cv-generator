# Futurice CV Generator

Note, you need to add copies of some Sharp Sans fonts under `fonts/` to use with Docker or have them installed in your system font storage for usage locally.

## Sample CV 
This tool can generate a C.V. that looks like the following. In both PDF or PNG formats. 

![cv 1](https://cloud.githubusercontent.com/assets/7697632/26059407/5ec64372-398a-11e7-95cc-8090a47076c3.png)


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

## License

Copyright (C) 2016  Futurice

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
