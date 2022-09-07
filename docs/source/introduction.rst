.. include:: <isonum.txt>

Introduction
============

*powfacpy* is a wrapper around the Python API of PowerFactory |copy| (software for power system simulation by DIgSILENT). 
You can automate almost anything in PowerFactory |copy| with the native API, but the syntax can be verbose. Therefore, 
*powfacpy* provides features and interface classes to make your life easier.

For example, setting attributes of an object in the PowerFactory |copy| database requires several lines of code with the 
native API. With the API of *powfacpy*, this is only one line:

.. code::

   set_attr(r"Network Model\Network Data\Grid\Terminal MV",{"uknom":33,"outserv":0})

Here we have set two attributes (uknom, outserv) of the object specified under the path "Network Mod...".

Plotting also requires many lines with the native API (need to add the variable to the monitored variables, create a 
plot page, add the curve,..). However, using *powfacpy* the syntax is succinct and similar to matplotlib. Just activate 
a plot and then plot variables of an object:

.. code::

   set_active_plot("Active power","§ PV plant")
   plot(r"Network Model\Network Data\Grid\PV", "m:Psum:bus1")

*powfacpy* will save you time and make your code more readable.
Get started with the :ref:`tutorials` or see a list of classes and methods under :ref:`api`.

The module is at an early stage. Contributions (new features, bug reports, feature requests, etc.) are very welcome on Github. 

Installation
------------
Using pip:

.. code::

   pip install powfacpy

Contact
----------
*simon.eberlein@iee.fraunhofer.de*

About
----------

This module is under active development.

*powfacpy* is an open source module which is mainly developed at Fraunhofer IEE and not associated with DIgSILENT.