pip install uwsgi
uwsgi --http :10000 --wsgi-file app.py --callable app
