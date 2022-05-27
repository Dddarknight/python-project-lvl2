make lint: #запуск flake8
	poetry run flake8 gendiff

install:
	poetry install

test-coverage:
	poetry run pytest --cov=gendiff