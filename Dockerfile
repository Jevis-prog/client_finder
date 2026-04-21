FROM python:3.12-slim

ENV \
  TZ=Europe/Moscow \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN apt-get update && apt-get install -y \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY pip/requirements.txt pip/constraints.txt ./
RUN pip install -c constraints.txt -r requirements.txt

COPY . .

CMD sh -c "sleep infinity"
