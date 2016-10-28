schools:
	honcho run python manage.py dumpdata planner.School --indent 2 -o planner/fixtures/schools.json

deploy:
	ansible-playbook -i playbooks/production playbooks/site.yml

galaxy:
	ansible-galaxy install \
		Datadog.datadog \
		kamaln7.swapfile \
		nodesource.node

seed:
	ansible-playbook \
		--private-key=./.vagrant/machines/default/virtualbox/private_key \
		-i playbooks/development playbooks/seed.yml
