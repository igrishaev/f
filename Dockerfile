FROM python:2.7
ADD f /app/f
ADD tests /app/tests
COPY pip.requirements* /app/
WORKDIR /app
RUN pip install -r pip.requirements.test
RUN find . -name "*pyc" -delete
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH .
CMD py.test tests
