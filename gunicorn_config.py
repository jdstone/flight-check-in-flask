import os


workers = int(os.getenv('GUNICORN_PROCESSES', '2'))
threads = int(os.getenv('GUNICORN_THREADS', '4'))
bind = f"{os.getenv('GUNICORN_IP', '0.0.0.0')}:{os.getenv('GUNICORN_PORT', '8080')}"
