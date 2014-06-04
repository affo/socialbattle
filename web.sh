#!/bin/bash

if [ $API == 1 ]; then
	python manage.py runserver 0.0.0.0:$PORT --noreload
else
	node site/server.js
fi

#BUILDPACK_URL=https://github.com/heroku/heroku-buildpack-nodejs
#BUILDPACK_URL=https://github.com/heroku/heroku-buildpack-python