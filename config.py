

# Celery configuration
config={}
config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"