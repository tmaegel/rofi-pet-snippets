SRC_PATH = rofi_pet_snippets

run:
	rofi -show snippets -modi "snippets:venv/bin/rofi-pet-snippets"

install:
	pip install --user .

install_dev:
	pip install -e .

test:
	coverage run -m pytest
	coverage report

tox:
	tox -e py39

lint:
	python -m flake8
	pylint $(SRC_PATH)
	python -m mypy .

pre-commit:
	pre-commit run --all-files
