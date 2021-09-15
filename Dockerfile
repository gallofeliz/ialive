FROM python:3.8-alpine3.12

RUN python3 -m pip install influxdb

ADD app.py .

CMD python ./app.py
