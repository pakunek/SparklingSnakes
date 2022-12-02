PYTHON_BIN := python3
PIP := pip

APP_NAME := sparkling-snakes-processor
PACKAGE_DIR_NAME := sparkling_snakes

DOCKER_COMPOSE := docker-compose -f
DOCKER_COMPOSE_FILE := docker-compose.yml

VENV := venv

all: venv

$(VENV)/bin/activate: requirements-env.txt
	$(PYTHON_BIN) -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements-env.txt

venv: $(VENV)/bin/activate

build: clean_build
	$(PYTHON_BIN) setup.py sdist
	$(PYTHON_BIN) setup.py bdist_wheel

install_env:
	$(PIP) install -r requirements-env.txt

install:
	$(PIP) install ./dist/sparkling_snakes*.whl --force-reinstall

run:
	uvicorn sparkling_snakes.main:app --host 0.0.0.0

test: venv
	# TODO: Add basic unit tests

lint: venv
	flake8 ./$(PACKAGE_DIR_NAME) ./test
	mypy ./$(PACKAGE_DIR_NAME) --strict

clean: clean_build clean_pyc clean_venv
	rm -rf $(PACKAGE_DIR_NAME).egg-info
	rm -rf .mypy_cache

clean_build:
	rm -rf build dist || true

clean_pyc:
	find . -type f -name '*.pyc' -delete

clean_venv:
	rm -rf $(VENV)

docker_build: docker_build_pyspark docker_build_sparkling_snakes

docker_build_pyspark:
	docker build -f dockerfiles/pyspark/Dockerfile -t pyspark-cluster .

docker_build_sparkling_snakes:
	docker build -f dockerfiles/sparkling_snakes/Dockerfile -t sparkling-snakes-processor .

docker_up:
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) up -d

docker_up_sparkling_snakes:
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) up -d processor

docker_down_sparkling_snakes:
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) stop processor

docker_down:
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) down

.PHONY: all venv build install run test lint clean clean_build clean_pyc clean_venv docker_build docker_build_pyspark docker_build_sparkling_snakes docker_up docker_up_sparkling_snakes docker_down_sparkling_snakes docker_down