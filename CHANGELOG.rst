
Changelog
=========

0.1.0 (2018-03-20)
------------------

* First release on PyPI.

0.1.1 (2018-04-13)
------------------

* Flak8-compliant

0.1.2 (2018-04-14)
------------------

* added --source and --destination options to the command line
* source file can be followed (like 'tail -f ') with --follow
* destination file can contain only the last messaget (with --snapshot)
* destinations abstracted in emittargets.py

0.1.3 (2018-04-14) (unreleased)
-------------------------------

*  made read/write mode detection more sophisticated: --source and --destination will 
   overrule the detection of detected STDIN / STDOUT redirection (this makes it
   easier to run mqttcat inside docker)
*  input and output are now compatible with JSON streams defined in RFC7464_ - those
   can be processed with jq_, for example


.. _RFC7464: https://tools.ietf.org/html/rfc7464
.. _jq: https://stedolan.github.io/jq/ 
