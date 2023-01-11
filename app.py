from flask import Flask, request
import redis
import os
from rq import Queue
from jobs import simple_background_task, init_model
from utils import generate_large_file
import time

app = Flask(__name__)

r = redis.Redis()
queue_default = Queue(connection=r)
queue_bigfile_loading = Queue(name="bigfile_loading", connection=r)

large_file_path = "large_file.txt"


@app.route("/init_model")
def init():
    job = queue_bigfile_loading.enqueue(init_model, args=(), meta={'start_time': time.time()})
    q_len = len(queue_bigfile_loading)
    return f"Task {job.id} added to queue {job.origin} at {job.enqueued_at}. {q_len} tasks in the queue"


@app.route("/task")
def add_task():
    if request.args.get("n"):
        job = queue_default.enqueue(simple_background_task, args=(request.args.get("n"),))
        q_len = len(queue_default)
        return f"Task {job.id} added to queue at {job.enqueued_at}. {q_len} tasks in the queue"

    return "No value for n"


@app.route("/tasks")
def add_multiple_tasks():
    if request.args.get("n"):
        for n in range(int(request.args.get("n"))):
            job = queue_bigfile_loading.enqueue(simple_background_task, args=(n,))
        q_len = len(queue_bigfile_loading)
        return f"{q_len} tasks in the queue"

    return "No value for n"


if __name__ == '__main__':
    if not os.path.exists(large_file_path):
        generate_large_file(large_file_path)
    app.run()
