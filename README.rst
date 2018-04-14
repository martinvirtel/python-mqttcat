========
Overview
========

Netcat for MQTT

* Free software: BSD 2-Clause License

============
Installation
============

This needs Python 3.6. At the command line::

    pip3 install mqttcat

If your system does not provide python 3.6, a more comfortable way is to use the mqtttool Docker 
container. Please see the `Github repo`_.


=============
Documentation
=============



::


    Usage: mqttcat [OPTIONS] URL

      A MQTT Message filter inspired by netcat and other Unix tools.

      Publishes Messages from STDIN to a MQTT Topic

        -or-

      Subscribes to MQTT Topic and writes messages to STDOUT

      URL - Examples:

          mqtt://hostname/topic     tcp://hostname:1883/topic
          ws://hostname/topic

      Usage Examples:

          mqttcat --echo mqtt://localhost/%23 >/dev/null

          ... will subscribe to all topics ("%23" is urlencoded #), and echo
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
      --loglevel TEXT             Python loglevel, one of
                                  DEBUG,INFO,WARNING,ERROR,CRITICAL
      --echo / --no-echo          Echo MQTT Messages to STDERR
      --source TEXT               File to read MQTT messages to be published (use
                                  '-' for STDIN)
      --wait FLOAT                Wait time between publishing messages read from
                                  --source in seconds (can be float)
      --loop / --no-loop          Loop message publishing (starting at beginning
                                  of file after the end is reached
      --follow / --no-follow      Wait for additional in file after reaching the
                                  end (like Unix 'tail -f')
      --destination TEXT          Append JSON-encoded MQTT messages to this file
                                  (use '-' for STDOUT)
      --snapshot / --no-snapshot  Keep only the last JSON-encoded message in the
                                  file specified with --destination
      --help                      Show this message and exit.



=======
Authors
=======

* Martin Virtel - https://twitter.com/mvtango

This module is part of the `Smart Orchestra Project`_, co-financed by the 
`Federal Ministery of Economics and Technology`_.


.. _Smart Orchestra Project: http://smartorchestra.de

.. _Github repo: https://github.com/martinvirtel/docker-mqtttool

.. _Federal Ministery of Economics and Technology: https://www.bmwi.de/
