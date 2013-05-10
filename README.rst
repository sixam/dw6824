==================================
dw6824 - A peer-to-peer whiteboard
==================================


What is it?
===========

dw6824 is a distributed peer-to-peer whiteboard. You can use it to draw anything
with your friends and colleagues.

Getting Started
===============

You need to install python >= 2.7.4 and PyQt4.

If you want to run the application, you should checkout the `app branch <https://github.com/atacchet/dw6824/tree/app>`_. 
Provided you have the right dependencies, you can just execute 

::
    
    $> python src/main.py.

To start a session click on the ``Session`` menu and chose ``Start Session...`` click ``OK``.
Tell your friends fo Join your session by providing them with the session number that will pop-up.

To join a session, click on the ``Session`` menu and choose ``Join Session``, click ``OK`` on the server address pop-up and 
then enter your session number and click ``OK``.

To leave a session, simply close the window.

If you get an error when you start or join a session, it might be that you are off-line or that I am not running the
central server. Shoot me an email.

If you want to run your own central server, see below.

Status
======

This is Andrea and Mika's final project for 6.824 at MIT. There is a **lot** to be done
to turn this into a fully functional application.

Developers' guide
=================

If you are interested in developing the application, there are a couple of things that you need to do before executing.
Here is a list of commands that should get you up and running

::

    $> cd ~/code
    $> git clone git@github.com:atacchet/dw6824.git
    $> mv dw6824 dp
    $> cd dp
    $> export DW_BASE=/home/atacchet/code/dp
    $> export PYTHONPATH=/home/atacchet/code:$PYTHONPATH
    $> mkdir log

These steps will result in a persistent log of all your sessions saved in the ``log`` directory.

If you want to run our test suite, install `nosetests <https://nose.readthedocs.org/en/latest/>`_.
For some reason our test suite crashes on Ubuntu but you can execute tests one by one.
It should work on MacOS.

If you want to run your own central server, have a look at code in the ``session`` directory.

Contribute
==========

If you want to contribute, here a list of stuff that we feel should be taken care of.

* Replicate the central server.
* Package all operations sent to a peer in a single RPC.
* Write a better join/leave protocol.
* Implement UNDO.

License
=======

Copyright (c) M. Gharbi and A. Tacchetti 2013. All Rights Reserved.

See the LICENSE file for the terms of the "New BSD License".

Credits
=======

We borrowed some ideas and data structures from `OpenCoweb <http://opencoweb.org/>`_.

We are thankful to R. Morris, N. Narula and C. Gruenwald for their help during 6.824 - Spring 2013.

References
==========

The operational transformation algorithm we used is based on:

* \D. Sun and C. Sun: "Context-based Operational Transformation in Distributed
  Collaborative Editing Systems," in IEEE Transactions on Parallel and
  Distributed Systems, Vol. 20, No. 10, pp. 1454 – 1470, Oct. 2009.

