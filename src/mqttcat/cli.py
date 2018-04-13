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
@click.argument('url')
def run(url, loglevel, echo, loop, wait):
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
    if echo:
        echostream = sys.stderr
    else:
        echostream = False
    t = MqttTopic(url, echo=echostream)
    if not sys.stdout.isatty():
        logger.info("Subscribed to {} - messages will be written to STDOUT".format(t.topic))
        t.subscribe()
        import time
        while True:
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                break
    elif not sys.stdin.isatty():
        logger.info("Reading from STDIN - publishing messages to {} [loop:{loop},wait:{wait} sec.]".format(t.topic, **locals()))
        t.publish(t.feeder(sys.stdin, loop=loop), wait=wait, echo=echo)
    else:
        print("STDIN and STDOUT are ttys - no action taken. Use --help for help")


if __name__ == '__main__':
    run()
