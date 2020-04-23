test:
	PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 pytest -v

run:
	PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 FLASK_APP=nestorfire.adapters.http.endpoints.py FLASK_ENV=development pipenv run flask run
	
create-fire:
	http post http://localhost:5000/fires lat=32.5435 lon=11.2333

lint:
	flake8

reformat:
	black nestorfire