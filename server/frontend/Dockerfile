FROM python:3.8.7-slim-buster

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt


EXPOSE 8501

CMD ["streamlit", "run", "main.py"]