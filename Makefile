SHELL := /bin/bash


TESTNETWORK := mqtt-test-network

mosquitto :
	docker run --rm --name mosquitto --network=$(TESTNETWORK) --network-alias=mosquitto -ti -p 1883:1883 -p 9001:9001 \
			toke/mosquitto

distribute:
	python setup.py bdist upload
