FROM python:2.7
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /app

COPY pip.requirements* /
WORKDIR /
RUN pip install -r pip.requirements.dev
RUN rm pip.requirements*

WORKDIR /app
