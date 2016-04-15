schools:
	honcho run python manage.py dumpdata planner.School --indent 2 -o planner/fixtures/schools.json

run:
	python manage.py runserver 8080

test:
	honcho run python manage.py test
