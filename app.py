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

import galileo_task as g_task

app = Flask(__name__)
app.config["SECRET_KEY"] = "top-secret!"


@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        return render_template("index.html", email=session.get("email", ""))


@app.route("/longtask", methods=["POST"])
def longtask():
    task = g_task.long_task.apply_async()
    return jsonify({}), 202, {"Location": url_for("taskstatus", task_id=task.id)}


@app.route("/status/<task_id>")
def taskstatus(task_id):
    task = g_task.long_task.AsyncResult(task_id)
    print(task.state)
    print(task.info)
    print(task.info.get("status"))

    if task.state == "PENDING":
        response = {
            "state": task.state,
            "current": 0,
            "total": 1,
            "status": "Pending...",
        }
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "current": task.info.get("current", 0),
            "total": task.info.get("total", 1),
            "status": task.info.get("status", ""),
        }
        if "result" in task.info:
            response["result"] = task.info["result"]
    else:
        # something went wrong in the background job
        response = {
            "state": task.state,
            "current": 1,
            "total": 1,
            "status": str(task.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, use_reloader=True)
