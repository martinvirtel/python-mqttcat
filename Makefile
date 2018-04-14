SHELL := /bin/bash

MQTTSERVICE := mosquitto
TESTNETWORK := mqtt-test-network


network: 
	test "$(TESTNETWORK)" = "$$(docker network ls --filter name=$(TESTNETWORK) --format '{{.Name}}')" || docker network create $(TESTNETWORK)

mosquitto :
	test "$(MQTTSERVICE)" = "$$(docker ps --filter name=$(MQTTSERVICE) --format '{{.Names}}')" || \
	docker run --rm --name $(MQTTSERVICE) --network=$(TESTNETWORK) --network-alias=$(MQTTSERVICE) -ti -p 1883:1883 -p 9001:9001 \
	toke/mosquitto


monitor: mosquitto
	mqttcat mqtt://localhost/%23 --loglevel=DEBUG --echo >/dev/null

heartbeat: mosquitto
	printf "tick\ntock\n" | mqttcat mqtt://localhost/heartbeat --loop --wait=1


distribute:
	python setup.py sdist upload
