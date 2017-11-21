FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv cron nginx git

# RUN pyvenv venv && . venv/bin/activate && pip install --upgrade pip

RUN mkdir -p /opt/NNReversi/django && cd /opt/NNReversi \
    && mkdir -p /var/run/nnreversi /var/log/nnreversi \
    && chown www-data:www-data /var/run/nnreversi /var/log/nnreversi

COPY django /opt/NNReversi/django
COPY environment/nnreversi.conf /etc/nginx/sites-available/nnreversi.conf

RUN rm /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/nnreversi.conf /etc/nginx/sites-enabled/nnreversi.conf \
    && touch /opt/NNReversi/django/django.log && chown -R www-data.www-data /opt/NNReversi/django

RUN cd /opt/NNReversi && pyvenv venv && . venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r /opt/NNReversi/django/requirements.txt

STOPSIGNAL SIGTERM

WORKDIR /opt/NNReversi/django

CMD . /opt/NNReversi/venv/bin/activate \
  && service nginx restart \
  && uwsgi --ini /opt/NNReversi/django/mysite/uwsgi.ini
