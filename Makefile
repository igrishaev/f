
test:
	PYTHONPATH=. py.test tests/ -s -x

pep:
	flake8 .
