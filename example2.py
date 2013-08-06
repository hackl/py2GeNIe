#!/usr/bin/python -tt
# -*- coding: utf-8 -*-


from py2GeNIe import *


  # Define a main() function.
def main():

  # Create a Network
  net = Network('Network')

  # Create Node 'Success'
  success = Node('Success')

  # Setting number (and name) of outcomes
  success.addOutcome('Success')
  success.addOutcome('Failure')

  # Create node 'Forecast'
  forecast = Node('Forecast')

  # Setting number (and name) of outcomes
  forecast.addOutcomes(['Good','Moderate','Poor'])

  # Add arc from 'Success' to 'Forecast'
  arc = Arc(success,forecast)

  # Shows the size of the probability matrix
  #print forecast.getTableSize()

  # Conditional distribution for node 'Success'
  success.setProbabilities([0.1,0.9])

  # Conditional distribution for node 'Forecast'
  forecast.setProbabilities([0.4, 0.4, 0.2, 0.1, 0.3, 0.6])

  # Add decision Invest
  invest = Decision('Invest')

  # Setting number (and name) of outcomes
  invest.addOutcomes(['Invest','DonotInvest'])

  # Add utility Financial Gain
  gain = Utility('Gain')

  # Add arc from 'Invest' and 'Succsess' to 'Gain'
  arc_S_G = Arc(success,gain)
  arc_I_G = Arc(invest,gain)

  # Conditional distribution for node 'Forecast'
  gain.setUtilities([10000, 500, -5000, 500])

  # Changing the nodes spacial and visual attributes:
  success.setNodePosition(250,10)
  success.setInteriorColor('ff9900')

  forecast.setNodePosition(250,150)
  forecast.setInteriorColor('ff99cc')

  invest.setNodePosition(50,10)
  invest.setInteriorColor('c0c0c0')

  gain.setNodePosition(50,150)
  gain.setInteriorColor('99ccff')

  # Add notes to network
  net.addNodes([success,forecast,invest,gain])

  # Write file
  net.writeFile('tutorial2.xdsl')


  # This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

