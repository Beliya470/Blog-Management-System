pip install uwsgi
uwsgi --http :8000 --wsgi-file app.py --callable app
