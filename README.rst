========
PyWMTemp
========

WindowMaker dockapp for monitoring resources like CPU/GPU temperatures. It
supports up to 2 different readings.

.. image:: /images/pywmtemp.gif?raw=true
   :alt: wmamixer overview


Requirements
============

* Python
* wmdocklib
* psutil

Note, that you'll need to install `this wmdocklib`_ instead of original
`pywmdockapps`_, since the latter works only with Python2.


Installation
============

For now, use virtualenv:

.. code:: shell-session

   $ python -m virtualenv venv
   $ . venv/bin/activate
   (venv) $ pip install .


Usage
=====

You'll need to prepare yaml file with the configuration. And put it in
``~/.config/pywmtemp.yaml`` (or whatever your XDG_CONFIG_HOME points to). For
example:

.. code:: yaml

   ---
   readings:
     - sensor: k10temp
       label: Tccd1
       name: cpu
       override_warning: 65
       override_critical: 70
       unit: °C
     - sensor: amdgpu
       label: edge
       name: gpu
       override_warning: 60
       override_critical: 70
       unit: °C

This will look for the two separate temperatures, one for AMD Ryzen CPU,
second for Radeon graphic card. Your hardware might vary, see the output of:

.. code:: shell-session

   $ python -c 'import psutil; import pprint; pprint.pprint(psutil.sensors_temperatures())'

There are six supported keys in the config:

- sensor - case sensitive sensor name, it corresponds for the keys in
  dictionary returned by ``psutil.sensors_temperatures()``
- label - it's a unique label for the sensor reading, all the ``shwtemp``
  namedtuples should have it. Case sensitive.
- name - name displayed on the dockapp. It will be uppercased.
- unit - it should be always °C
- override_warning - if not set, ``high`` value from shwtemp would be used if
  exists.
- override_warning - if not set, ``critical`` value from shwtemp would be used
  if exists.

Those last keys will set the threshold when color for the temperature line will
change.

By clicking with the left mouse button on the graph region, it will switch
between those two readings.

You can create only one entry if you like. If you create more than two entries
in config, all above first two will be ignored. You can, however, run multiple
instances of this dockapp by passing different configs using ``--config``
parameter.


License
=======

This software is licensed under 3-clause BSD license. See LICENSE file for
details.


.. _this wmdocklib: https://github.com/gryf/wmdocklib
.. _pywmdockapps: https://github.com/mfrasca/pywmdockapps
