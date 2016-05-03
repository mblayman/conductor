schools:
	honcho run python manage.py dumpdata planner.School --indent 2 -o planner/fixtures/schools.json

run:
	python manage.py runserver 8080

shell:
	honcho run python manage.py shell

test:
	honcho run python manage.py test

deploy:
	ansible-playbook -i playbooks/production playbooks/site.yml

galaxy:
	ansible-galaxy install \
		kamaln7.swapfile \
		nodesource.node

bootstrap:
	ansible-playbook \
		--private-key=./.vagrant/machines/default/virtualbox/private_key \
		-i playbooks/development playbooks/bootstrap.yml -vvvv
