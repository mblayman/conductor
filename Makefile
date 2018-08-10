.PHONY: frontend

deploy:
	ansible-playbook -i playbooks/production playbooks/site.yml

frontend:
	cd frontend && \
	npm run watch

galaxy:
	ansible-galaxy install \
		Datadog.datadog \
		kamaln7.swapfile \
		nodesource.node

mypy:
	@git ls-files | grep '.py$$' | grep -v 'migrations' | xargs mypy

schools:
	honcho run python manage.py dumpdata planner.School --indent 2 -o planner/fixtures/schools.json

seed:
	ansible-playbook \
		--private-key=./.vagrant/machines/default/virtualbox/private_key \
		-i playbooks/development playbooks/seed.yml
