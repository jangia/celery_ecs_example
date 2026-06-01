###########
# BUILDER #
###########

FROM python:3.12-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get -y install --no-install-recommends g++ \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev


#########
# FINAL #
#########

FROM python:3.12-slim-bookworm

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get -y install --no-install-recommends lsof \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system app && adduser --system --group app

ENV HOME=/home/app \
    APP_HOME=/home/app/web \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=prod \
    TESTING=0 \
    PATH="/opt/venv/bin:$PATH" \
    VIRTUAL_ENV=/opt/venv

RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

COPY --from=builder /opt/venv /opt/venv
COPY . $APP_HOME

ENV PYTHONPATH=$APP_HOME

RUN chown -R app:app $HOME /opt/venv

USER app
