FROM arm32v7/python:slim

RUN mkdir /app

WORKDIR /app

#COPY requirements.txt /app/

RUN apt-get update -y && \
    apt-get install -y libmosquitto-dev libbluetooth-dev libffi-dev gcc make && \
    pip3 install paho-mqtt pybluez && \
#   pip3 install -r requirements.txt && \
    apt-get purge -y gcc make && \
    apt-get autoremove -y && \
    rm -rf /root/.cache/ && \
    rm -rf /var/lib/apt /var/lib/dpkg

COPY *.py /app/

CMD ["/app/bluemaestro_mqtt.py"]
