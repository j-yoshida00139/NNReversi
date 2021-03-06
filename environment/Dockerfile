FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv cron nginx git libmysqlclient-dev

RUN mkdir -p /opt/NNReversi/django && cd /opt/NNReversi \
    && mkdir -p /var/run/nnreversi /var/log/nnreversi \
    && chown www-data:www-data /var/run/nnreversi /var/log/nnreversi \
    && touch /var/log/nnreversi/debug.log && chmod -R 777 /var/log/nnreversi

COPY environment/requirements.txt /opt/NNReversi/requirements.txt

RUN cd /opt/NNReversi && pyvenv venv && . venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r /opt/NNReversi/requirements.txt

COPY django /opt/NNReversi/django
COPY environment/nnreversi.conf /etc/nginx/sites-available/nnreversi.conf

RUN rm /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/nnreversi.conf /etc/nginx/sites-enabled/nnreversi.conf \
    && touch /opt/NNReversi/django/django.log && chown -R www-data.www-data /opt/NNReversi/django

STOPSIGNAL SIGTERM

WORKDIR /opt/NNReversi/django

CMD . /opt/NNReversi/venv/bin/activate \
  && service nginx restart \
  && uwsgi --ini /opt/NNReversi/django/mysite/uwsgi.ini
