FROM python:3.13.0-alpine3.20

WORKDIR /flight-check-in-flask

ENV TZ=America/Los_Angeles

COPY requirements.txt /flight-check-in-flask/
COPY config.py /flight-check-in-flask/
COPY gunicorn_config.py /flight-check-in-flask/
COPY VERSION /flight-check-in-flask/
COPY app/ /flight-check-in-flask/app/

RUN pip3 install -r requirements.txt &&\
 ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENTRYPOINT ["gunicorn"]
CMD ["--config", "gunicorn_config.py", "app:create_app()"]

