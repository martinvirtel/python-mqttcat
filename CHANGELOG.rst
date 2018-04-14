
Changelog
=========

0.1.0 (2018-03-20)
------------------

* First release on PyPI.

0.1.1 (2018-04-13)
------------------

* Flak8-compliant.

0.1.2 (2018-04-14)
------------------

* possible destinations abstractet in emittargets.py
* added the following switches to the command line tool:
  --source TEXT               File to read MQTT messages to be published (use
                              '-' for STDIN)
  --wait FLOAT                Wait time between publishing messages messages
                              in Seconds (can be float)
  --loop / --no-loop          Loop message publishing (starting at beginning
                              of file after the end is reached
  --follow / --no-follow      Wait for additional in file after reaching the
                              end (like Unix 'tail -f')


  --destination TEXT          Append JSON-encoded MQTT messages to this file
                              (use '-' for STDOUT)
  --snapshot / --no-snapshot  Instead of appending, keep only the last JSON-encoded 
                              message in the file specified with --destination

