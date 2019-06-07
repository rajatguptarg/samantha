init:
	pip install -r requirements.txt

test:
	python setup.py test
	flake8 .

build:
	python setup.py sdist

check:
	check-manifest

publish:
	python setup.py publish
