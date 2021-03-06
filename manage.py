from flask import Flask
from flask.cli import FlaskGroup
from server import create_app
import redis
from rq import Connection, Worker, Queue
from rq_scheduler import Scheduler
import datetime

from nestorfire.adapters.cli.import_fires import import_fires
from nestorfire.adapters.http.config import db

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
def view_scheduled_jobs():
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


@cli.command("create_db")
def create_db():
    print("Creating database ..")
    db.create_schema()
    print("done.")

'''
@cli.command("drop_db")
def drop_db():
    print("Dropping database ..")
    db.drop_schema()
    print("done.")
'''

@cli.command("create_tables")
def create_tables():
    print("Creating tables ..")
    db.create_tables()
    print("done.")

@cli.command("drop_tables")
def drop_tables():
    print("Dropping tables ..")
    db.drop_tables()
    print("done.")
    

if __name__ == "__main__":
    cli()