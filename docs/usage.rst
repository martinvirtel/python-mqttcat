=====
Usage
=====


Command Line Usage: mqttcat [OPTIONS] URL

  A Mqtt Message filter inspired by netcat and other unix tools.

  Publishes Messages from STDIN to Mqtt Topic

    -or-

  Subscribes to Mqtt Topic and writes messages to STDOUT

  URL - Examples:

      mqtt://hostname/topic     tcp://hostname:1883/topic
      ws://hostname/topic

  Usage Examples:

      mqttcat --echo mqtt://localhost/%23 >/dev/null

      ... will subscribe to all topics ("%24" is urlencoded #), and echo
      them to STDERR for control

      echo "Heart ... beat" | mqttcat --echo --loop --wait=3.3
      mqtt://localhost/heartbeat-topic

      ... will publish "Heart ... beat" every 3.3 seconds to the topic
      "heartbeat-topic"

      mqttcat mqtt://source/ticktock | rq 'filter (a) => { a.payload="tock"
      }' | mqttcat mqtt://destination/tock

      ... subscribe to ticktock topic on host source, filter out the
      messages whose payload is tock,     and forward those to the tock
      topic (using the rq tool https://github.com/dflemstr/rq)

Options:
  --loglevel TEXT     Python loglevel, one of
                      DEBUG,INFO,WARNING,ERROR,CRITICAL
  --echo / --no-echo  Echo Mqtt Messages to STDERR
  --wait FLOAT        Wait time between messages in Seconds (can be float)
  --loop / --no-loop  Loop output
  --help              Show this message and exit.
