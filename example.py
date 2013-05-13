#!/usr/bin/python -tt
# -*- coding: utf-8 -*-


from py2GeNIe import *


  # Define a main() function.
def main():

  # Create a Network
  net = GenieNetwork('Network')

  # Create Node 'Success'
  success = GenieNode('Success')

  # Setting number (and name) of outcomes
  success.addOutcome('Success')
  success.addOutcome('Failure')

  # Conditional distribution for node 'Success'
  success.setProbability([0.1,0.9])


  # Create node 'Forecast'
  forecast = GenieNode('Forecast')

  # Setting number (and name) of outcomes
  forecast.addOutcome('Good')
  forecast.addOutcome('Moderate')
  forecast.addOutcome('Poor')

  # Add arc from 'Success' to 'Forecast'
  arc = GenieArc(success,forecast)

  # Conditional distribution for node 'Forecast'
  forecast.setProbability([0.4, 0.4, 0.2, 0.1, 0.3, 0.6])

  # Changing the nodes spacial and visual attributes:
  success.setNodePosition(50,10)
  success.setInteriorColor('cc99ff')

  forecast.setNodePosition(50,150)
  forecast.setInteriorColor('ff0000')

  # Add notes to network
  net.addNodes([success,forecast])

  # Write file
  net.writeFile('tutorial.xdsl')


  # This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

