FROM python:3.7-slim

RUN adduser kerasuser

WORKDIR /home/keras_flask

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install pip==19.3.1
RUN venv/bin/pip install setuptools==41
RUN venv/bin/pip install -r requirements.txt
RUN apt-get update && apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev


COPY app app
COPY models models
COPY utils utils
COPY inference.py keras_api.py boot.sh ./
RUN chmod u+x boot.sh

ENV FLASK_APP keras_api.py

RUN chown -R kerasuser:kerasuser ./
USER kerasuser

EXPOSE 80

CMD . venv/bin/activate && exec gunicorn -b :5000 --access-logfile - --error-logfile - keras_api:app
