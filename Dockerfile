FROM python:alpine

RUN python3 -m pip install influxdb

ADD app.py .

CMD python ./app.py
