"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mmqttcat` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``mqttcat.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``mqttcat.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import click
import sys
import logging
from mqttcat import MqttTopic

logger = logging.getLogger(__name__)


def set_root_logger(loglevel):
    try:
        if type(loglevel) == int:
            level = loglevel
        else:
            level = getattr(logging, loglevel)
            assert(type(level) == int)
        logging.getLogger().setLevel(level)
    except Exception as e:
        raise ValueError("Failed setting log level to {}: {}".format(loglevel,
                         repr(e)))


@click.command()
@click.option('--loglevel', default="INFO",
              help="Python loglevel, one of DEBUG,INFO,WARNING,ERROR,CRITICAL")
@click.option('--echo/--no-echo',
              default=False,
              help="Echo Mqtt Messages to STDERR")
@click.option('--wait', type=float,
              default=0.1,
              help="Wait time between messages in Seconds (can be float)")
@click.option('--loop/--no-loop',
              default=False,
              help="Loop output")
@click.option('--source',
              default=None,
              help="Message source file (use '-' for STDIN)")
@click.option('--destination',
              default=None,
              help="Message source file (use '-' for STDOUT)")
@click.argument('url')
def run(url, source, destination, loglevel, echo, loop, wait):
    """
    A Mqtt Message filter inspired by netcat and other unix tools.

    Publishes Messages from STDIN to Mqtt Topic

      -or-

    Subscribes to Mqtt Topic and writes messages to STDOUT

    URL - Examples:

        mqtt://hostname/topic
        tcp://hostname:1883/topic
        ws://hostname/topic


    Usage Examples:

        mqttcat --echo mqtt://localhost/%23 >/dev/null

        ... will subscribe to all topics ("%24" is urlencoded #), and echo them to STDERR for control


        echo "Heart ... beat" | mqttcat --echo --loop --wait=3.3 mqtt://localhost/heartbeat-topic

        ... will publish "Heart ... beat" every 3.3 seconds to the topic "heartbeat-topic"


        mqttcat mqtt://source/ticktock | rq 'filter (a) => { a.payload="tock" }' | mqttcat mqtt://destination/tock

        ... subscribe to ticktock topic on host source, filter out the messages whose payload is tock,
        and forward those to the tock topic (using the rq tool https://github.com/dflemstr/rq)

    """
    set_root_logger(loglevel)
    # load_config(config)
    mode = None
    if echo:
        echostream = sys.stderr
    else:
        echostream = False
    if source == '-' or (source is None and not sys.stdin.isatty()):
        sourcestream = sys.stdin
        mode = 'read'
    else :
        if source is not None :
            sourcestream = open(source)
            mode = 'read'
    if mode is None :
        if destination == '-' or (destination is None and not sys.stdout.isatty()):
            deststream = sys.stdout
            mode = 'write'
        else :
            if destination is not None :
                deststream = open(destination,"w")
                mode = 'write'
    if mode == 'write':
        t = MqttTopic(url, echo=echostream,writer=deststream)
        logger.info("Subscribed to {} - messages will be written to {}".format(t.topic, deststream.name))
        t.subscribe()
        import time
        while True:
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                break
    elif mode == 'read' :
        t = MqttTopic(url, echo=echostream)
        logger.info("Reading from {sourcestream.name} - publishing messages to {} [loop:{loop},wait:{wait} sec.]".format(t.topic, **locals()))
        t.publish(MqttTopic.feeder(sourcestream, loop=loop), wait=wait, echo=echo)
    else:
        print("Could not determine wether to read or write. Use STDIN redirection or --source parameter to publish Mqtt messages. Use STDOUT redirection or --destination to subscribe to topic or topics.")


if __name__ == '__main__':
    run()
