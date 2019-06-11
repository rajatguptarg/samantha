init:
	pip install -r requirements.txt

test:
	coverage run setup.py test
	flake8 samantha
	coverage xml
	coverage report -m

build:
	python setup.py sdist

check:
	check-manifest

publish:
	python setup.py publish
