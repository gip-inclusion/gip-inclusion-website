ifeq ($(USE_VENV),1)
	EXEC_CMD :=
else
	EXEC_CMD := docker compose exec -ti web
endif

.PHONY: runserver
runserver:
	$(EXEC_CMD) python manage.py runserver

.PHONY: web-prompt
web-prompt:
	$(EXEC_CMD) bash

.PHONY: test-unit
test-unit:
	$(EXEC_CMD) python manage.py test --settings config.settings_test

.PHONY: test-e2e
test-e2e:
	$(EXEC_CMD) python manage.py behave --settings config.settings_test

.PHONY: test
test: test-e2e test-unit

.PHONY: quality
quality:
	$(EXEC_CMD) ruff format --check
	$(EXEC_CMD) ruff check
	$(EXEC_CMD) djlint --lint --check .

.PHONY: fix
fix:
	$(EXEC_CMD) ruff format
	$(EXEC_CMD) ruff check --fix
	$(EXEC_CMD) djlint --reformat templates
