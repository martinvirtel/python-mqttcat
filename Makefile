SHELL := /bin/bash

mosquitto :
	docker run --rm --name mosquitto -ti -p 1883:1883 -p 9001:9001 \
			toke/mosquitto

