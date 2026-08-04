.PHONY: help install build test run demo clean lint

DJANGO_SETTINGS ?= test_settings
PYTHON ?= .venv/bin/python
UV ?= uv

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-14s\033[0m %s\n", $$1, $$2}'

venv: ## Create virtual environment
	$(UV) venv

install: venv ## Install package in editable mode
	$(UV) pip install -e .

build: ## Build the wheel/sdist
	$(UV) build

test: ## Run the test suite
	$(PYTHON) -m django test npdt --settings=$(DJANGO_SETTINGS) -v2

test-quick: ## Run tests (fail fast)
	$(PYTHON) -m django test npdt --settings=$(DJANGO_SETTINGS) -v2 --no-input --failfast

run: ## Run Django dev server on port 8000
	$(PYTHON) manage.py runserver 0.0.0.0:8000 --settings=$(DJANGO_SETTINGS)

migrate: ## Run Django migrations
	$(PYTHON) manage.py migrate --settings=$(DJANGO_SETTINGS)

createsuperuser: ## Create a Django superuser
	$(PYTHON) manage.py createsuperuser --settings=$(DJANGO_SETTINGS)

shell: ## Open Django shell
	$(PYTHON) manage.py shell --settings=$(DJANGO_SETTINGS)

demo: ## Start the JS picker demo server on port 8081
	$(PYTHON) -m http.server 8081 --directory ../javascript

clean: ## Remove build artifacts and temp files
	rm -rf build/ dist/ *.egg-info .venv/ .pytest_cache/
	rm -f test_db.sqlite3
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true

lint: ## Run Python linter
	ruff check npdt/ example/ test_settings.py test_urls.py manage.py 2>/dev/null || \
		echo "No linter installed. Run: uv pip install ruff"

check: lint test ## Run lint + test
