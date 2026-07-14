import os

bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")
workers = int(os.getenv("GUNICORN_WORKERS", "1"))
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info").lower()