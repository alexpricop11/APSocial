FROM python:3.12

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /

RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app

COPY . /app/

CMD ["python", "server/manage.py", "runserver", "0.0.0.0:8000"]