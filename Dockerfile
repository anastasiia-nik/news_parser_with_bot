FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV C_FORCE_ROOT 1

WORKDIR /app/
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

CMD python manage.py runserver 127.0.0.1:8000

EXPOSE 8000