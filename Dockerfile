FROM ubuntu
# ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD . /code/
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install numpy django
EXPOSE 8000
# RUN pip install git+git://github.com/mverteuil/pytest-ipdb.git
RUN pip3 install -r requirements.txt
RUN python3 manage.py runserver 172.17.0.2:8000
