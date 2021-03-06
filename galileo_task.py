import os
import random
import time
from flask import (
    Flask,
    request,
    render_template,
    session,
    flash,
    redirect,
    url_for,
    jsonify,
)
from celery import Celery

# Celery configuration
config = {}

config["CELERY_BROKER_URL"] = os.getenv(
    'CELERY_BROKER_URL', 'redis://localhost:6379/0')
config["CELERY_RESULT_BACKEND"] = os.getenv(
    'CELERY_BROKER_URL', 'redis://localhost:6379/0')

print(config)

# Initialize Celery
celery = Celery("Galileo Task", broker=config["CELERY_BROKER_URL"])
celery.conf.update(config)


@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ["Starting up", "Booting", "Repairing", "Loading", "Checking"]
    adjective = ["master", "radiant", "silent", "harmonic", "fast"]
    noun = ["solar array", "particle reshaper", "cosmic ray", "orbiter", "bit"]

    message = ""
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = "{0} {1} {2}...".format(
                random.choice(verb), random.choice(
                    adjective), random.choice(noun)
            )
        self.update_state(
            state="PROGRESS", meta={"current": i, "total": total, "status": message}
        )
        time.sleep(1)

    return {"current": 100, "total": 100, "status": "Task completed!", "result": "100/100"}
