FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PORT 8001

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations --noinput || true
RUN python manage.py migrate --noinput || true

CMD python manage.py runserver 0.0.0.0:$PORT
