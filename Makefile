reset-db:
	psql -c 'DROP DATABASE giw;'
	psql -c 'ALTER USER giw CREATEDB;'
	psql -c 'CREATE DATABASE giw OWNER giw;'
	python manage.py migrate

.PHONY: web-prompt
web-prompt:
	docker-compose run --rm web bash

.PHONY: test-unit
test-unit:
	python manage.py test --settings git_inclusion_website.settings_test

.PHONY: test-e2e
test-e2e:
	python manage.py behave --settings git_inclusion_website.settings_test

.PHONY: test
test: test-e2e test-unit
