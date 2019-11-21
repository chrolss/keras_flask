FROM python:3.7-slim

WORKDIR /home/keras_flask

COPY requirements.txt requirements.txt

RUN pip install pip==19.3.1
RUN pip install setuptools==41
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev

COPY app app
COPY models models
COPY utils utils
COPY inference.py keras_api.py boot.sh ./
RUN chmod u+x boot.sh

ENV FLASK_APP keras_api.py
ENV NAME World


EXPOSE 80

CMD ["python", "keras_api.py"]
