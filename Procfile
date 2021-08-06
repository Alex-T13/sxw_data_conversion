release: python src/manage.py migrate
web: gunicorn --config="scripts/gunicorn.conf.py" project.wsgi:application
