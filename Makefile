make lint: #запуск flake8
	poetry run flake8 gendiff

install:
	poetry install

check: selfcheck test lint
