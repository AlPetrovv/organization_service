FROM python:3.14-slim


ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/home/app/src


RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev  \
    python3-dev

RUN useradd -m app

WORKDIR /home/app

RUN pip install --upgrade pip && pip install poetry
ADD pyproject.toml poetry.lock ./


ENV VIRTUAL_ENV=/app/.venv
RUN python -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN chown -R app:app /home/app/

USER app


