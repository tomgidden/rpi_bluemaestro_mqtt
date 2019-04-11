TAG=tomgidden/rpi_ugeek_cobber_mqtt
HOSTNAME=campi_inside

start:
	docker create --hostname $(HOSTNAME) --device /dev/i2c-1 --device /dev/mem --privileged --rm --name ugeek_cobber_mqtt  $(TAG)
	docker start ugeek_cobber_mqtt

stop:
	docker rm -f ugeek_cobber_mqtt

build: Dockerfile *.py requirements.txt
	docker build . -t $(TAG)

push:
	docker push $(TAG):latest

test:
	docker run --hostname $(HOSTNAME) -it --rm --privileged -v /dev/i2c-1:/dev/i2c-1 $(TAG) bash
