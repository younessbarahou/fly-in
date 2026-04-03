install:
	pip install -r ./requirements.txt
run:
	python3 main.py
lint:
	flake8 .
	mypy .
