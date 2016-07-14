
test:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. py.test tests/ -s -x -v

pep:
	flake8 .

clean:
	find . -name "*.pyc" -delete

build:
	python setup.py bdist_wheel --universal

register:
	python setup.py register -r pypi

upload:
	python setup.py bdist_wheel --universal upload -r pypi
