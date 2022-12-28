FROM python:3.8-slim

ENV DOCKER=true

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt
EXPOSE 8000