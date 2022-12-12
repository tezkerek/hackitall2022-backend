FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN mkdir /code/
WORKDIR /code/
COPY pyproject.toml /code/

RUN pip install poetry
RUN poetry install
