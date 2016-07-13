
test:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. py.test tests/ -s -x -v

pep:
	flake8 .

clean:
	find . -name "*.pyc" -delete
