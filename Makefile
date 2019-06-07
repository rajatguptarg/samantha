init:
	pip install -r requirements.txt

test:
	python setup.py test
	flake8 samantha

build:
	python setup.py sdist

check:
	check-manifest

publish:
	python setup.py publish
