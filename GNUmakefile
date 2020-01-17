TAG=tomgidden/rpi_bluemaestro_mqtt
HOSTNAME=campi_outside
NAME=rpi_bluemaestro_mqtt
MQTT_TOPIC=/sensor/uk/CB29JW/bluemaestro
MQTT_HOST=192.168.0.2

build: Dockerfile *.py requirements.txt
	docker build . -t $(TAG)

run:
	docker run \
			--hostname $(HOSTNAME) \
			--env MQTT_TOPIC=$(MQTT_TOPIC) \
			--env MQTT_HOST=$(MQTT_HOST) \
			--env MQTT_CLIENT_NAME=$(HOSTNAME) \
			--net host \
			--rm -it \
			--name $(NAME) \
			$(TAG)

kill:
	docker rm -f $(NAME)

test:
	docker run \
			--hostname $(HOSTNAME) \
			--env MQTT_TOPIC=$(MQTT_TOPIC) \
			--env MQTT_HOST=$(MQTT_HOST) \
			--env MQTT_CLIENT_NAME=$(HOSTNAME) \
			--net host \
			--rm -it \
			--name $(NAME) \
			$(TAG) \
			bash

install-systemd:
	sudo cp bluemaestro_mqtt_docker.service /etc/systemd/system
	sudo systemctl daemon-reload

start-systemd:
	sudo systemctl start bluemaestro_mqtt_docker

stop-systemd:
	sudo systemctl stop bluemaestro_mqtt_docker

status-systemd:
	sudo systemctl status bluemaestro_mqtt_docker --no-pager --full
	sudo journalctl -u bluemaestro_mqtt_docker -f

logs:
	docker logs $(NAME)

push:
	docker push $(TAG):latest
