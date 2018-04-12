__version__ = '0.1.0'

import click
import json
import logging
import sys
import time
import os
import urllib.parse
from functools import partial
from collections import OrderedDict
import csv
import paho.mqtt.client


logger=logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,stream=sys.stderr,
         format="%(asctime)-15s %(name)s %(levelname)s %(filename)s:%(lineno)s %(message)s")

# logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.CRITICAL)




import base64

def to_data(bstr) :
    return "data:;base64,{}".format(base64.b64encode(bstr).encode('ascii'))




class MqttTopic(object) :

    __slots__ = ('url','kwargs','client','topic','echo')


    def __init__(self,url,echo=None,**kwargs) :
        parsed=urllib.parse.urlsplit(url)
        if parsed.scheme in ('ws','websockets') :
            kwargs["transport"]='websockets'
        self.kwargs=kwargs
        import paho.mqtt.client
        client=paho.mqtt.client.Client(**kwargs)
        client.connect(parsed.hostname,parsed.port if parsed.port else 1883)
        client.on_message=partial(MqttTopic.read,self)
        client.loop_start()
        self.client=client
        self.topic = urllib.parse.unquote(parsed.path[1:])
        self.echo=echo
        logger.debug("Connected to {url} {kwargs}".format(**locals()))


    def subscribe(self) :
        self.client.subscribe(self.topic)


    def read(self,client,userdata,message) :
        obj=dict()
        for a in ("qos","topic","payload","timestamp") :
            val = getattr(message,a)
            if type(val) == bytes :
                try :
                    val = val.decode("utf-8")
                except Exception:
                    val = to_data(val)
            obj[a]=val
        repr=json.dumps(obj) + "\n"
        sys.stdout.write(repr)
        sys.stdout.flush()
        if hasattr(self.echo,'write') :
            self.echo.write(repr)


    def publish(self,dicts,wait=None,echo=None) :
        for current in dicts :
            self.client.publish(self.topic,current["payload"])
            if hasattr(echo,'write') :
                self.echo.write(json.dumps(current)+"\n")
            if wait == True :
                raise NotImplementedError("Missing: copy wait time from input stream")
            elif float(wait) > 0 :
                time.sleep(wait)


    def feeder(self,stream,loop=False) :
        buf=[]
        logger.debug(f"starting feeder")
        for line in iter(stream.readline,None) :
            if line is None :
                break
            try :
                current=json.loads(line)
            except Exception as e:
                logger.debug(f"{line} not decoded as JSON: {e}")
                current=dict(payload=line[:-1])
            if loop :
                buf.append(current)

            yield(current)
        if loop:
            while True :
                for current in buf:
                    yield current

    def __del__(self) :
        try :
            self.client.disconnect()
        except Exception as e :
            logger.debug(f"Error disconnecting: {e}")
        else :
            try:
                self.client.loop_stop()
            except Exception as e:
                logger.debug(f"Error stopping loop: {e}")




protocols={
            'MQTTv31'  : paho.mqtt.client.MQTTv31,
            'MQTTv311' : paho.mqtt.client.MQTTv311
          }



