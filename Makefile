
test:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. py.test tests/ -s -x -v

pep:
	flake8 .

pyc:
	find . -name "*.pyc" -delete
