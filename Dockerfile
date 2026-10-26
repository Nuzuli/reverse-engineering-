FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --create-home --shell /usr/sbin/nologin analyst

WORKDIR /app
COPY src/ ./src/

USER analyst
ENTRYPOINT ["python", "-m", "src.analyzer"]