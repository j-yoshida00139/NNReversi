FROM ubuntu

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv cron nginx git \
    && mkdir -p /opt/NNReversi && cd /opt/NNReversi \
    && pyvenv venv && . venv/bin/activate && pip install --upgrade pip \
    && mkdir -p /var/run/nnreversi /var/log/nnreversi \
    && chown www-data:www-data /var/run/nnreversi /var/log/nnreversi

COPY . /opt/NNReversi/
COPY nnreversi.conf /etc/nginx/sites-available/nnreversi.conf

RUN rm /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/nnreversi.conf /etc/nginx/sites-enabled/nnreversi.conf \
    && cd /opt/NNReversi && . venv/bin/activate \
    && pip install -r /opt/NNReversi/requirements.txt \
    && touch /opt/NNReversi/django.log && chown -R www-data.www-data /opt/NNReversi

EXPOSE 80

STOPSIGNAL SIGTERM

WORKDIR /opt/NNReversi

CMD . /opt/NNReversi/venv/bin/activate \
  && service nginx restart \
  && uwsgi --ini /opt/NNReversi/mysite/uwsgi.ini
