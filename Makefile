SRC_PATH = rofi_pet_snippets

run:
	rofi -show snippets -modi "snippets:./$(SRC_PATH)/__init__.py"

install:
	pip install --user .

test:
	python -m pytest
	python -m pytest --cov --cov-fail-under=75

lint:
	python -m flake8
	python -m mypy $(SRC_PATH)

pre-commit:
	pre-commit run --all-files

install_dev:
	pip install -r requirements_dev.txt
