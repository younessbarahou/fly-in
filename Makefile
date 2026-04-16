install:
	poetry install
run:
	python3 parsing.py
lint:
	flake8 .
	mypy .
clean:
	rm -rf __pycach__ .mypy_cache