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
	python manage.py test --settings config.settings_test

.PHONY: test-e2e
test-e2e:
	python manage.py behave --settings config.settings_test

.PHONY: test
test: test-e2e test-unit

.PHONY: quality
quality:
	black --check --exclude=venv .
	isort --check --skip-glob="**/migrations" --extend-skip-glob="venv" .
	flake8 --count --show-source --statistics --exclude=venv .
	djlint --lint --check --use-gitignore .

.PHONY: fix
fix:
	black --exclude=venv .
	isort --skip-glob="**/migrations" --extend-skip-glob="venv" .
	djlint --reformat --use-gitignore .
