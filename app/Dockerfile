FROM python:3.7-slim

LABEL app="devopstom-flask-website"

RUN apt-get -y update && apt-get -y install build-essential \
    python3-dev

COPY requirments.txt /home/app/
RUN pip install -r /home/app/requirments.txt

COPY app.py /home/app/
COPY helpers /home/app/helpers/
COPY templates /home/app/templates/
COPY uwsgi/uwsgi.ini /home/app/
WORKDIR /home/app
RUN chown -R www-data:www-data .

CMD ["/usr/local/bin/uwsgi", "/home/app/uwsgi.ini"]

ARG CI_COMMIT_REF_SLUG=local
ENV CI_COMMIT_REF_SLUG=$CI_COMMIT_REF_SLUG

ARG CI_COMMIT_SHORT_SHA=local
ENV CI_COMMIT_SHORT_SHA=$CI_COMMIT_SHORT_SHA

ARG CI_COMMIT_TAG=local
ENV CI_COMMIT_TAG=$CI_COMMIT_TAG