TAG=tomgidden/rpi_bluemaestro_mqtt
HOSTNAME=campi_outside
NAME=rpi_bluemaestro_mqtt

run:
	docker create \
			--hostname $(HOSTNAME) \
			--env MQTT_TOPIC=/sensor/uk/CB29JW/bluemaestro \
			--env MQTT_HOST=mqtt.home \
			--env MQTT_CLIENT_NAME=$(HOSTNAME) \
			--net host \
			--rm -it \
			--name $(NAME) $(TAG)
	docker start $(NAME)

install-systemd:
	sudo cp bluemaestro_mqtt_docker.service /etc/systemd/system
	sudo systemctl daemon-reload
	sudo systemctl start bluemaestro_mqtt_docker

start-systemd:
	sudo systemctl start bluemaestro_mqtt_docker

stop-systemd:
	sudo systemctl stop bluemaestro_mqtt_docker

status-systemd:
	sudo systemctl status bluemaestro_mqtt_docker --no-pager --full
	sudo journalctl -u bluemaestro_mqtt_docker -f

status-docker:
	docker logs $(NAME)

kill:
	docker rm -f $(NAME)

build: Dockerfile *.py requirements.txt
	docker build . -t $(TAG)

push:
	docker push $(TAG):latest

test:
	docker run \
			--hostname $(HOSTNAME) \
			--env MQTT_TOPIC=/sensor/uk/CB29JW/bluemaestro \
			--env MQTT_HOST=mqtt.home \
			--env MQTT_CLIENT_NAME=$(HOSTNAME) \
			--net host \
			--rm -it \
			$(TAG) \
			bash
