.PHONY: help build test check clean lint \
       build-rust test-rust bench-rust \
       build-python test-python \
       build-js test-js demo-js \
       build-django test-django run-django \
       build-all test-all

CARGO ?= cargo
UV ?= uv

# ── Help ──────────────────────────────────────────────────────────────

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

# ── Rust Core ─────────────────────────────────────────────────────────

build-rust: ## Build Rust core library
	$(CARGO) build --release

test-rust: ## Run Rust tests
	$(CARGO) test

bench-rust: ## Run Rust benchmarks
	$(CARGO) bench

lint-rust: ## Lint Rust code
	$(CARGO) clippy -- -D warnings
	$(CARGO) fmt -- --check

# ── Python Bindings ──────────────────────────────────────────────────

build-python: ## Build Python wheel (maturin)
	cd bindings/python && $(UV) build

test-python: ## Run Python binding tests
	cd bindings/python && $(CARGO) test --features python

# ── JavaScript / WASM Bindings ───────────────────────────────────────

build-js: ## Build WASM package (wasm-pack)
	cd bindings/javascript && wasm-pack build --target web

test-js: ## Run JS/WASM tests
	cd bindings/javascript && wasm-pack test --node

demo-js: build-js ## Build WASM + start JS picker demo on :8081
	@echo "Demo running at http://localhost:8081/demo/index.html"
	cd bindings/javascript && python3 -m http.server 8081

# ── Django Bindings ──────────────────────────────────────────────────

DJANGO_DIR := bindings/django
DJANGO_PYTHON := .venv/bin/python
DJANGO_SETTINGS := test_settings

build-django: build-js ## Build WASM + install Django package in editable mode
	cd $(DJANGO_DIR) && $(UV) venv && $(UV) pip install -e .
	@echo "Syncing JS/CSS assets to Django static..."
	cp bindings/javascript/picker.js $(DJANGO_DIR)/npdt/static/npdt/js/picker.min.js
	cp bindings/javascript/picker.css $(DJANGO_DIR)/npdt/static/npdt/css/picker.css
	rm -rf $(DJANGO_DIR)/npdt/static/npdt/js/pkg
	cp -r bindings/javascript/pkg $(DJANGO_DIR)/npdt/static/npdt/js/pkg

test-django: ## Run Django test suite
	cd $(DJANGO_DIR) && $(DJANGO_PYTHON) -m django test npdt --settings=$(DJANGO_SETTINGS) -v2

run-django: ## Run Django dev server on :8000
	cd $(DJANGO_DIR) && $(DJANGO_PYTHON) manage.py runserver 0.0.0.0:8000 --settings=$(DJANGO_SETTINGS)

migrate-django: ## Run Django migrations
	cd $(DJANGO_DIR) && $(DJANGO_PYTHON) manage.py migrate --settings=$(DJANGO_SETTINGS)

shell-django: ## Open Django shell
	cd $(DJANGO_DIR) && $(DJANGO_PYTHON) manage.py shell --settings=$(DJANGO_SETTINGS)

# ── Aggregate Targets ────────────────────────────────────────────────

build: build-rust ## Build Rust core (default)

build-all: build-rust build-js build-django ## Build everything

test: test-rust ## Run Rust tests (default)

test-all: test-rust test-django ## Run all tests

check: lint-rust test-rust ## Lint + test Rust

lint: lint-rust ## Lint Rust code

# ── Clean ─────────────────────────────────────────────────────────────

clean: ## Remove all build artifacts
	$(CARGO) clean
	rm -rf bindings/django/.venv/ bindings/django/build/ bindings/django/dist/
	rm -rf bindings/django/*.egg-info bindings/django/test_db.sqlite3
	rm -rf pkg/ target/
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
