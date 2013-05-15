.. _chap_tutorial:

********
Tutorial
********

This tutorial is based on `Java Tutorial 1 Creating a Bayesian Network`_:

Creating a Bayesian Network
===========================

The first step is the initialization of the network. ::

  # Create a Network
  net = Network('Network')

Now the nodes for the Bayesian Network can be created. ::

  # Create Node 'Success'
  success = Node('Success')

This node should have two states. Let us name them Success and Failure. ::

  # Setting number (and name) of outcomes
  success.addOutcome('Success')
  success.addOutcome('Failure')

The number and name of the outcomes belongs to the definition of the node. We
can (and must) define them before any useful inference can be made on the
network. Following the same procedure for the node Forecast, we create a new
node and let it have three states: ::

  # Create node 'Forecast'
  forecast = Node('Forecast')

  # Setting number (and name) of outcomes
  forecast.addOutcome('Good')
  forecast.addOutcome('Moderate')
  forecast.addOutcome('Poor')

We can do this also in one step: ::

  # Setting number (and name) of outcomes
  forecast.addOutcomes(['Good','Moderate','Poor'])  

Now, we can add an arc from Success to Forecast to represent the conditional
dependence of the latter on the former. ::

  # Add arc from 'Success' to 'Forecast'
  arc = Arc(success,forecast)

Now we need to fill in the distribution of the nodes. We know that the node
Success has two states and no parents, so we just need two numbers that
represent the probability of each of the states coming true. ::

  # Conditional distribution for node 'Success'
  success.setProbabilities([0.1,0.9])

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

  forecast.setProbabilities([0.4, 0.4, 0.2, 0.1, 0.3, 0.6])

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
retrieve it later. The format of the file will be XDSL. If no file name is
chosen, the network name will be used. ::

  # Write file
  net.writeFile('tutorial.xdsl')


Finally...
==========

This was a short introduction how to use ``py2GeNIe``. The tutorial above is also
available on `GitHub`_ under ``example.py``.

If you like to learn more about `GeNIe`_ visit http://genie.sis.pitt.edu/

Let's have fun ;)


.. _`GeNIe`: http://genie.sis.pitt.edu/

.. _`Java Tutorial 1 Creating a Bayesian Network`: http://genie.sis.pitt.edu/wiki/Java_Tutorials:_Tutorial_1:_Creating_a_Bayesian_Network

.. _`GitHub`: https://github.com/hackl/py2GeNIe
