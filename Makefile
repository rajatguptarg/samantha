init:
	pip3 install -r requirements.txt

test:
	coverage run setup.py test
	flake8 samantha
	coverage xml
	coverage report -m

build:
	python3 setup.py sdist

check:
	check-manifest

publish:
	python3 setup.py publish
