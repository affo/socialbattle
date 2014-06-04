#!/bin/bash

if [ "$API" == "true" ]; then
	python manage.py runserver 0.0.0.0:$PORT --noreload
else
	node site/server.js
fi