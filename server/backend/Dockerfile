FROM python:3.8.7-slim-buster

WORKDIR /app
COPY . /app
ENV PYTHONPATH=/app
ENV PYTHONBUFFERED=1

RUN pip install pip==21.2.4 && \
    pip install -r requirements.txt

CMD ["python", "main.py"]
