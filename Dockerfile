FROM arm32v7/python:slim

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update -y && \
    apt-get install -y libmosquitto-dev libffi-dev gcc make && \
    pip3 install -r requirements.txt && \
    apt-get purge -y gcc make && \
    rm -rf /root/.cache/ && \
    rm -rf /var/lib/apt /var/lib/dpkg

COPY *.py /app/

CMD ["/app/ugeek_cobber_mqtt.py"]
