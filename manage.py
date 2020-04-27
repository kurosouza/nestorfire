from flask import Flask
from flask.cli import FlaskGroup
from server import create_app
import redis
from rq import Connection, Worker, Queue
from rq_scheduler import Scheduler
import datetime

from nestorfire.adapters.cli.import_fires import import_fires

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command("start_worker")
def start_worker():
    redis_url = app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection) as conn:
        worker = Worker(app.config['QUEUES'])
        worker.work()

@cli.command("schedule_jobs")
def schedule_jobs():
    with Connection(redis.from_url(app.config['REDIS_URL'])) as conn:
        q = Queue()
        scheduler = Scheduler(queue=q)
        scheduler.schedule(scheduled_time=datetime.datetime.utcnow(),
        func=import_fires,
        interval= 5 * 60,
        repeat=3
        )

@cli.command("view_scheduled_jobs")
def view_schedules_jobs():
    with Connection(redis.from_url(app.config['REDIS_URL'])) as conn:
        q = Queue()
        scheduler = Scheduler(connection=conn)
        jobs_list = scheduler.get_jobs()
        for j in jobs_list:
            print(j)

@cli.command("run_import_fires")
def run_import_fires():
    with Connection(redis.from_url(app.config['REDIS_URL'])) as con:
        q = Queue()
        task = q.enqueue(import_fires)

if __name__ == "__main__":
    cli()