FROM python:3.8.7-slim-buster

WORKDIR /app
COPY . /app

ENV PYTHONPATH=/app
ENV PYTHONBUFFERED=1

RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
RUN apt-get -y install libglib2.0-0

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]
