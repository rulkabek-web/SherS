FROM mcr.microsoft.com/playwright/python:v1.61.0-noble

ARG TEST_PROFILE=api
ARG BACKEND_URL=http://host.docker.internal:4111/api
ARG DATABASE_URL=postgresql+psycopg2://symfony:password@host.docker.internal:5432/symfony_db

ENV TEST_PROFILE=${TEST_PROFILE}
ENV BACKEND_URL=${BACKEND_URL}
ENV DATABASE_URL=${DATABASE_URL}

WORKDIR /app

copy requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD pytest -m "api or ui" --alluredir=/app/reports/allure