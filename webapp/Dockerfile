FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./app /app
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt
