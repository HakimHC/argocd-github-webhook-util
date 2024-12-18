FROM python:3.11-alpine
LABEL author=HakimHC

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    APP_HOME=/app

WORKDIR $APP_HOME

RUN apk add --no-cache \
    gcc \
    g++ \
    libffi-dev \
    musl-dev \
    openssl-dev && \
    pip install --upgrade pip

COPY requirements.txt $APP_HOME/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . $APP_HOME

RUN adduser -D flask && \
    chown -R flask:flask $APP_HOME

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0", "src.main:app"]
