FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV C_FORCE_ROOT 1

WORKDIR /app/
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:8000

EXPOSE 8000