web: python manage.py runserver 0.0.0.0:$PORT --noreload
worker: celery worker --app=socialbattle -l info --broker=$CLOUDAMQP_URL