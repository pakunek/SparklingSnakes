PYTHON_BIN := /usr/bin/python3

PACKAGE_DIR_NAME := sparkling_snakes

VENV := venv

all: venv

$(VENV)/bin/activate: requirements-venv.txt
	$(PYTHON_BIN) -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements-venv.txt

venv: $(VENV)/bin/activate

build: clean_build venv
	$(PYTHON_BIN) setup.py sdist
	$(PYTHON_BIN) setup.py bdist_wheel

test: venv
	# TODO: Add basic unit tests

coverage: venv
	# TODO: Add basic coverage

lint: venv
	mypy ./$(PACKAGE_DIR_NAME) --strict
	flake8 ./$(PACKAGE_DIR_NAME) ./test

clean: clean_build clean_pyc clean_venv
	rm -rf $(PACKAGE_DIR_NAME).egg-info
	rm -rf .mypy_cache

clean_build:
	rm -rf build dist

clean_pyc:
	find . -type f -name '*.pyc' -delete

clean_venv:
	rm -rf $(VENV)

docker_build: docker_build_pyspark

docker_build_pyspark:
	docker build -f dockerfiles/pyspark/Dockerfile -t pyspark-cluster .

docker_build_sparkling_snakes:
	docker build -f dockerfiles/sparkling_snakes/Dockerfile -t sparkling-snakes-processor .

docker_up:
	docker-compose -f docker-compose.yml up -d

docker_down:
	docker-compose -f docker-compose.yml down

.PHONY: all venv build test coverage lint clean clean_build clean_pyc clean_venv docker_build docker_build_pyspark docker_up docker_down