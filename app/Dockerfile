FROM python:3.7-slim

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
