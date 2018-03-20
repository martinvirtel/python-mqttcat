__version__ = '0.1.0'

import click
import json
import logging
import sys
import time
import os
import copy
import jmespath
import urllib.parse
from functools import partial
from collections import OrderedDict
import csv
import paho.mqtt.client


logger=logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,stream=sys.stderr,
         format="%(asctime)-15s %(name)s %(levelname)s %(filename)s:%(lineno)s %(message)s")

# logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.CRITICAL)


here=os.path.split(__file__)[0]


def set_root_logger(loglevel) :
    try :
        if type(loglevel)==int :
            level=loglevel
        else :
            level=getattr(logging,loglevel)
            assert(type(level)==int)
        logging.getLogger().setLevel(level)
    except Exception as e:
        raise ValueError("Failed setting log level to {}: {}".format(loglevel,repr(e)))

import base64

def to_data(bstr) :
    return "data:;base64,{}".format(base64.b64encode(bstr).encode('ascii'))

class MqttTopic(object) :

    __slots__ = ('url','kwargs','client','topic','echo')


    def __init__(self,url,echo=None,**kwargs) :
        parsed=urllib.parse.urlsplit(url)
        if parsed.scheme in ('tls','websockets') :
            kwargs["transport"]=parsed.scheme
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
        if self.echo is not None :
            self.echo.write(repr)



    def __del__(self) :
        self.client.disconnect()
        self.client.loop_stop()




protocols={
            'MQTTv31'  : paho.mqtt.client.MQTTv31,
            'MQTTv311' : paho.mqtt.client.MQTTv311
          }


@click.command()
@click.option('--loglevel',default="INFO",
                           help="Python loglevel, one of DEBUG,INFO,WARNING,ERROR,CRITICAL")
@click.option('--echo', type=click.Choice([None, 'stderr']),
                          default=None,
                          help="Output Format")
@click.argument('url')
def run(url,loglevel,echo) :
    global Config
    set_root_logger(loglevel)
    # load_config(config)
    if echo is not None :
        echo=sys.stderr
    t=MqttTopic(url,echo=echo)
    if not sys.stdout.isatty() :
        logger.info("Subscribed to {} - echoing to STDOUT".format(t.topic))
        t.subscribe()
        import time
        while True :
            try :
                time.sleep(10)
            except KeyboardInterrupt :
                break














if __name__=="__main__" :
    run()


