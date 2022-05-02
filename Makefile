SRC_PATH = rofi_pet_snippets

run:
	rofi -show snippets -modi "snippets:./$(SRC_PATH)/__init__.py"

install:
	pip install --user .

test:
	coverage run -m pytest
	coverage report

tox:
	tox -e py39

lint:
	python -m flake8
	python -m mypy $(SRC_PATH)

pre-commit:
	pre-commit run --all-files

install_dev:
	pip install -r requirements_dev.txt
