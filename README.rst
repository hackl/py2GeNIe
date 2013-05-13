********
py2GeNIe
********

:Date: 12 May 2013
:Authors: Jürgen Hackl
:Contact: hackl.j@gmx.at
:Web site: http://github.com/hackl/py2GeNIe
:Copyright: This document has been placed in the public domain.
:License: py2GeNIe is released under the GNU General Public Licence.
:Version: 1.0

Purpose
=======

``py2GeNIe`` converts python files to `GeNIe`_ input files.

Getting Started
===============

Installation
------------

Clone this (or a forked version of this) repository. ::

  $ git clone https://github.com/hackl/py2GeNIe.git

Import ``py2GeNIe`` in the python file. ::

  from py2GeNIe improt *

Tutorial
--------

This tutorial is based on `SMILE Tutorial 1 Creating a Bayesian Network`_

The first step is the initialization of the network. ::

  # Create a Network
  net = GenieNetwork('Network')

Now the nodes for the Bayesian Network can be created. ::

  # Create Node 'Success'
  success = GenieNode('Success')

This node should have two states. Let us name them Success and Failure. ::

  # Setting number (and name) of outcomes
  success.addOutcome('Success')
  success.addOutcome('Failure')

The number and name of the outcomes belongs to the definition of the node. We
can (and must) define them before any useful inference can be made on the
network. Following the same procedure for the node Forecast, we create a new
node and let it have three states: ::

  # Create node 'Forecast'
  forecast = GenieNode('Forecast')

  # Setting number (and name) of outcomes
  forecast.addOutcome('Good')
  forecast.addOutcome('Moderate')
  forecast.addOutcome('Poor')

Now, we can add an arc from Success to Forecast to represent the conditional
dependence of the latter on the former. ::

  # Add arc from 'Success' to 'Forecast'
  arc = GenieArc(success,forecast)

Now we need to fill in the distribution of the nodes. We know that the node
Success has two states and no parents, so we just need two numbers that
represent the probability of each of the states coming true. ::

  # Conditional distribution for node 'Success'
  success.setProbability([0.1,0.9])

Now we have to fill the distribution of the node Forecast conditioned on the
node Success. Definition matrix in this case, will have two dimensions: one
for the states of the parent (Success) and one for the states of the child
(Forecast).

If you not sure about the size of the matrix, you can check the size with
``forecast.getTableSize()``.

The order of these probabilities is given by considering the state of the
first parent of the node as the most significant (thinking of the coordinates
in terms of bits) coordinate, then the second parent, then the third (and so
on), and finally considering the coordinate of the node itself as the least
significant one.::

  forecast.setProbability([0.4, 0.4, 0.2, 0.1, 0.3, 0.6])

After the network has been created we make it more spatially organized and
change a few visual nodes' attributes. ::

  # Changing the nodes spacial and visual attributes:
  success.setNodePosition(50,10)
  success.setInteriorColor('cc99ff')

  forecast.setNodePosition(50,150)
  forecast.setInteriorColor('ff0000')

Finally we have to add the nodes to the network. ::

  # Add notes to network
  net.addNodes([success,forecast])

Now we can store the network in a file called "tutorial.xdsl" so we can
retrieve it later. The format of the file will be XDSL. ::

  # Write file
  net.writeFile('tutorial.xdsl')

List of References
==================

[GeNIe] Decision Systems Laboratory of the University of Pittsburgh, 2013. URL http://genie.sis.pitt.edu/




.. _`GeNIe`: http://genie.sis.pitt.edu/

.. _`SMILE Tutorial 1 Creating a Bayesian Network`: http://genie.sis.pitt.edu/wiki/SMILE_Tutorial_1:_Creating_a_Bayesian_Network
