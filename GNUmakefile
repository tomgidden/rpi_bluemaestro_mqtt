TAG=tomgidden/rpi_bluemaestro_mqtt
HOSTNAME=campi_outside

start:
	docker create --hostname $(HOSTNAME) --net host --rm --name bluemaestro_mqtt  $(TAG)
	docker start bluemaestro_mqtt

stop:
	docker rm -f bluemaestro_mqtt

build: Dockerfile *.py requirements.txt
	docker build . -t $(TAG)

push:
	docker push $(TAG):latest

test:
	docker run --hostname $(HOSTNAME) --net host -it --rm $(TAG) bash
