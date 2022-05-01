SRC_PATH = rofi_pet_snippets
VENV = ./venv

run:
	rofi -show snippets -modi "snippets:./rofi_pet_snippets.py"

install:
	cp -v rofi_pet_snippets.py ~/.local/bin/

test:
	python -m pytest

lint:
	python -m flake8 --max-line-length=88
	python -m mypy .

coverage:
	python -m pytest --cov --cov-fail-under=75

pre-commit:
	pre-commit run --all-files

install_dev:
	pip install -r requirements_dev.txt
