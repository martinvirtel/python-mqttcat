"""
Module that contains the command line app.

"""
import click
import sys
import logging
from mqttcat import MqttTopic
from mqttcat.emittarget import AppendToFile, SnapshotToFile

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
              help="Echo MQTT Messages to STDERR")
@click.option('--source',
              default=None,
              help="File to read MQTT messages to be published (use '-' for STDIN)")
@click.option('--wait', type=float,
              default=0.1,
              help="Wait time between publishing messages from --source in seconds (can be float)")
@click.option('--loop/--no-loop',
              default=False,
              help="Loop message publishing (starting at beginning of file after the end is reached")
@click.option('--follow/--no-follow',
              default=False,
              help="Wait for additional in file after reaching the end (like Unix 'tail -f')")
@click.option('--destination',
              default=None,
              help="Append JSON-encoded MQTT messages to this file (use '-' for STDOUT)")
@click.option('--snapshot/--no-snapshot',
              default=False,
              help="Keep only the last JSON-encoded message in the file specified with --destination")
@click.argument('url')
def run(url, source, follow, destination, snapshot, loglevel, echo, loop, wait):
    """
    A MQTT Message filter inspired by netcat and other Unix tools.

    Publishes Messages from STDIN to a MQTT Topic

      -or-

    Subscribes to MQTT Topic and writes messages to STDOUT

    URL - Examples:

        mqtt://hostname/topic
        tcp://hostname:1883/topic
        ws://hostname/topic


    Usage Examples:

        mqttcat --echo mqtt://localhost/%23 >/dev/null

        ... will subscribe to all topics ("%23" is urlencoded #), and echo them to STDERR for control


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
    else:
        if source is not None:
            sourcestream = open(source)
            mode = 'read'
    if mode is None:
        if snapshot:
            tclass = SnapshotToFile
        else:
            tclass = AppendToFile
        if destination == '-' or (destination is None and not sys.stdout.isatty()):
            deststream = tclass(sys.stdout)
            mode = 'write'
        else:
            if destination is not None:
                deststream = tclass(destination)
                mode = 'write'
    if mode == 'write':
        t = MqttTopic(url, echo=echostream, target=deststream)
        logger.info("Subscribed to {} - messages will be written to {}".format(t.topic, deststream))
        t.subscribe()
        import time
        while True:
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                break
    elif mode == 'read':
        t = MqttTopic(url, echo=echostream)
        logger.info("Reading from {sourcestream.name} - publishing messages to {} [loop:{loop},wait:{wait} sec.]".format(
                    t.topic, **locals()))
        t.publish(MqttTopic.feeder(sourcestream, loop=loop, follow=follow), wait=wait, echo=echo)
    else:
        print("""
        Could not determine wether to read or write.
        Use STDIN redirection or --source parameter to publish Mqtt messages.
        Use STDOUT redirection or --destination to subscribe to topic or topics.""")


if __name__ == '__main__':
    run()
