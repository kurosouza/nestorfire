test:
	PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 pytest -v

run:
	PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 FLASK_APP=nestorfire.adapters.http.endpoints.py FLASK_ENV=development pipenv run flask run
	
create-fire:
	http post http://localhost:5000/fires lat=32.5435 lon=11.2333

view-fires:
	http get http://localhost:5000/fires?limit=20&offset=20

lint:
	flake8

reformat:
	black nestorfire

start:
	docker-compose up -d

stop:
	docker-compose down

schedule-job:
	docker-compose exec api python manage.py schedule_jobs

view-scheduled-jobs:
	docker-compose exec api python manage.py view_scheduled_jobs

dbview:
	docker-compose exec postgis psql -Atx postgresql://user:secret@localhost:5432/gis

create_database:
	docker-compose exec api python manage.py create_db

# drop_database:
#	docker-compose exec api python manage.py drop_db
