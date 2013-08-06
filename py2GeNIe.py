#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Time-stamp: <Tue 2013-08-06 12:00 juergen>

import sys
import gc

class Network(object):
  """Bayesian Network

  :Attributes:
    - name (str): Name of the network
  """

  def __init__(self, name):
    self.name = repEmptySpace(name)
    self.nodes = []

  def __repr__(self):
    return self.name

  def addNode(self, node):
    """Add one node to the network

    :Args:
      - node (Node): Node element
    """
    self.nodes.append(node)

  def addNodes(self,nodes):
    """Add a list of nodes to the network

    :Args:
      - nodes (list): A list of Node elements
    """
    for node in nodes:
      self.addNode(node)

  def writeFile(self,filename=None):
    """Write an output file

    :Args:
      - filename (str): Name of the outputfile, If no name is defined the name of the network will be used.

    :Returns:
      - outputfile: The output files is saved in the local folder.

    :Raises:
      - Error: No nodes connected to the network!
      - Error: Node 'xy' has no outcomes!
      - Error: Probabilities for 'xy' doesn't match!\n
        Len of probabilities should be a but is b
      - Error: Probabilities for 'xy' doesn't sum up to 1.0!

    """
    self.checkInput()
    if filename == None:
      filename = self.name+'.xdsl'
    f = open(filename,'w')
    f.writelines(self.writeHeader())
    for node in self.nodes:
      f.write(node.printNode())
    f.writelines(self.writeBody())
    for node in self.nodes:
      f.write(node.printExtension())
    f.writelines(self.writeFooter())
    f.close()

  def writeHeader(self):
    header = ['<?xml version="1.0" encoding="ISO-8859-1"?>\n',
              '<smile version="1.0" id="'+self.name+'" numsamples="1000" discsamples="10000">\n',
              '\t<nodes>\n']
    return header

  def writeBody(self):
    body = ['\t</nodes>\n','\t<extensions>\n','\t\t<genie version="1.0" app="py2GeNIe 2013" name="'+self.name+'" faultnameformat="nodestate">\n']
    return body

  def writeFooter(self):
    footer = ['\t\t</genie>\n','\t</extensions>\n','</smile>']
    return footer


  def checkInput(self):
    if self.nodes == []:
      sys.exit("Error: No nodes connected to the network!")
    else:
      for node in self.nodes:
        if not (isinstance(node, Decision) or isinstance(node, Utility)):
          if node.getOutcomes() == []:
            sys.exit("Error: Node '"+str(node)+"' has no outcomes!")
          m,n = node.getTableSize()
          nodeLen = m*n
          if len(node.getProbabilities()) != nodeLen:
            sys.exit("Error: Probabilities for '"+str(node)+"' doesn't match!\n       Len of probabilities should be "+str(nodeLen)+" but is "+str(len(node.getProbabilities())))
          if sum(node.getProbabilities()) != n:
            sys.exit("Error: Probabilities for '"+str(node)+"' doesn't sum up to 1.0!")

class Node(object):
  """Node element for the Bayesian Network

  :Attributes:
    - name (str): Name of the node
  """
  nextIdNum = 0

  def __init__(self, name):
    self.name = repEmptySpace(name)
    self.caption = name
    self.idNum = Node.nextIdNum
    self.nodeId = 'Node_'+str(self.idNum)
    Node.nextIdNum += 1
    self.outcomes = []
    self.probabilities = []
    self.nextIdOut = 0
    self.arcConnection = []

    self.interior_color = 'e5f6f7'
    self.outline_color = '0000bb'
    self.font_color = '000000'
    self.font_name = 'Arial'
    self.font_size = 8
    self.node_size = [0,0,125,65]
    self.node_position = [0,0,125,65]
    self.bar_active = False
    """View as Bar Chart

    :Default:
      - ``False``: i.e. GeNIe will show Icons instead Bar Charts by default
    """

  def __repr__(self):
    return self.name

  def addOutcome(self,name):
    """Add one outcome to the node

    :Args:
      - name (str): Name of the outcome
    """
    self.outcomes.append(repEmptySpace(name))

  def addOutcomes(self,names):
    """Add a list of outcomes to the node

    :Args:
      - names (list): A list of names for the outcomes
    """
    for name in names:
      self.outcomes.append(repEmptySpace(name))

  def getOutcomes(self):
    """Returns a list of outcomes

    :Returns:
      - outcomes (list): Returns a list of outcomes
    """
    return self.outcomes

  def setProbabilities(self,probabilities):
    """Set the pobabilities for the node

    The order of these probabilities is given by considering the state of the
    first parent of the node as the most significant coordinate, then the
    second parent, then the third (and so on), and finally considering the
    coordinate of the node itself as the least significant one.

    :Args:
      - probabilities (list): A list of probabilities for the node
    """
    self.probabilities = probabilities

  def getProbabilities(self):
    """Returns a list of probabilities

    :Returns:
      - probabilities (list): Returns a list of probabilities
    """
    return self.probabilities

  def getProbability(self,index):
    """Returns a single probabilitiy

    :Args:
      - index (int): Position in the list of probabilities

    :Returns:
      - probabilitiy (float): Returns a single probabilitiy out of the list of probabilities
    """
    return self.probabilities[index]

  def addArcConnection(self,name,size):
    self.arcConnection.append([name,size])

  def getTableSize(self):
    """Returns the size of the probability table

    :Retunrs:
     - m,n (tuple): m represents the rows (number of outcomes)\n
       n represents the columns (depending from the parents and their outcomes)
    """
    if self.arcConnection == []:
      size = (self.getSize(),1)
    else:
      n = 1
      for i in range(len(self.arcConnection)):
        n *= self.arcConnection[i][1]
      size = (self.getSize(),n)
    return size

  def getTable(self):
    return self.tableSize

  def getSize(self):
    return len(self.outcomes)

  def printNode(self):
    # print node
    commentNode = '\t\t<!-- create node "'+self.caption+'" -->\n'
    initNode = '\t\t<cpt id="'+self.name+'" >\n'
    commentOutcomes = '\t\t\t<!-- setting names of outcomes -->\n'
    initOutcomes = ''
    for outcomes in self.outcomes:
      initOutcomes += '\t\t\t<state id="'+outcomes+'" />\n'

    if self.arcConnection != []:
      # print arc
      commentArc = '\t\t\t<!-- add arcs -->\n'
      initArc = '\t\t\t<parents>'
      for i in range(len(self.arcConnection)):
        initArc += self.arcConnection[i][0]+' '
      endArc =  '</parents>\n'
    else:
      commentArc = ''
      initArc = ''
      endArc = ''

    # print probabilities
    commentProbabilities = '\t\t\t<!-- setting probabilities -->\n'
    initProbabilities = '\t\t\t<probabilities>'
    for i,probability in enumerate(self.probabilities):
      initProbabilities += str(probability)+' '
    endProbabilities = '</probabilities>\n'
    endNode = '\t\t</cpt>\n'
    print_node =  commentNode+initNode+commentOutcomes+initOutcomes+commentArc+initArc+endArc+commentProbabilities+initProbabilities+endProbabilities+endNode
    return print_node

  def printExtension(self):
    initExtensions = '\t\t\t<node id="'+self.name+'">\n'
    initName = '\t\t\t\t<name>'+self.caption+'</name>\n'
    initIcolor = '\t\t\t\t<interior color="'+self.interior_color+'" />\n'
    initOcolor = '\t\t\t\t<outline color="'+self.outline_color+'" />\n'
    initFont = '\t\t\t\t<font color="'+self.font_color+'" name="'+self.font_name+'" size="'+str(self.font_size)+'" />\n'
    initPos = '\t\t\t\t<position>'+str(self.node_position[0])+' '+str(self.node_position[1])+' '+str(self.node_position[2])+' '+str(self.node_position[3])+'</position>\n'
    initBar = ''
    if self.bar_active == True:
      initBar = '\t\t\t\t<barchart active="true" width="'+str(self.node_size[2])+'" height="'+str(self.node_size[3])+'" />\n'
    endExtensions = '\t\t\t</node>\n'
    return initExtensions+initName+initIcolor+initOcolor+initFont+initPos+initBar+endExtensions

  def printProbabilities(self):
    commentProbabilities = '// setting probabilities for "'+self.name+'"\ntheProbs.Flush();\n'
    initProbabilities = 'theProbs.SetSize('+str(len(self.probability))+');\n'
    for i,probability in enumerate(self.probability):
      initProbabilities += 'theProbs['+str(i)+'] = '+str(probability)+';\n'
    endProbabilities = 'theNet.GetNode('+self.nodeId+')->Definition()->SetDefinition(theProbs);\n\n'
    print_prob = commentProbabilities+initProbabilities+endProbabilities
    return print_prob

  def getName(self):
    return self.name

  def getNodeId(self):
    return self.nodeId

  def setInteriorColor(self,interior_color):
    """Set interior color

    :Args:
      - interior_color (str): Interior color given as hex string

    :Example:
       >>>
       # red: rgb(255, 0, 0) -> ff0000
       xy.setInteriorColor('ff0000')
    """
    self.interior_color = interior_color

  def setOutlineColor(self,outline_color):
    """Set outline color

    :Args:
      - outline_color (str): Outline color given as hex string

    :Example:
       >>>
       # red: rgb(255, 0, 0) -> ff0000
       xy.setOutlineColor('ff0000')
    """
    self.outline_color = outline_color

  def setFontColor(self,font_color):
    """Set font color

    :Args:
      - font_color (str): Font color given as hex string

    :Example:
       >>>
       # red: rgb(255, 0, 0) -> ff0000
       xy.setFontColor('ff0000')
    """
    self.font_color = font_color

  def setFontName(self,font_name):
    """Set font name

    :Args:
      - font_name (str): Type of font, e.g. 'Arial', 'Times New Roman'
    """
    self.font_name = font_name

  def setFontSize(self,font_size):
    """Set font size

    :Args:
      - font_size (int): Size of font, e.g. 8, 12, ...
    """
    self.font_size = font_size

  def setNodeSize(self,x,y):
    """Set size of the node

    :Args:
      - x (int): Size in x direction
      - y (int): Size in y direction
    """
    self.node_size[2] = x
    self.node_size[3] = y

  def setNodePosition(self,x,y):
    """Set position of the node

    :Args:
      - x (int): Position in x direction
      - y (int): Position in y direction
    """
    self.node_position[0] = x
    self.node_position[1] = y
    self.node_position[2] = x+self.node_size[2]
    self.node_position[3] = y+self.node_size[3]

  def getNodePosition(self):
    return self.node_position

  def setBarActive(bar_active):
    """View node as Icon or Bar Chart

    :Args:
      - bar_active (boolean): ``True`` for Bar Chart view\n
        ``False`` for Icon view
    """
    self.bar_active = bar_active


class Arc(object):
  """Arc between two nodes

  :Attributes:
    - from_node (Node): Node where the arc starts
    - to_node (Node): Node where the arc points
  """

  def __init__(self, from_node, to_node):
    self.from_node = from_node
    self.to_node = to_node
    self.to_node.addArcConnection(self.from_node.getName(),self.from_node.getSize())

  def __repr__(self):
    return self.name



class Decision(Node):
  """Decision element for the Bayesian Network

  :Attributes:
    - name (str): Name of the node
  """

  def __init__(self, name):
    self.name = name
    Node.__init__(self,name)

  def printNode(self):
    # print node
    commentNode = '\t\t<!-- create decision "'+self.caption+'" -->\n'
    initNode = '\t\t<decision id="'+self.name+'" >\n'
    commentOutcomes = '\t\t\t<!-- setting names of outcomes -->\n'
    initOutcomes = ''
    for outcomes in self.outcomes:
      initOutcomes += '\t\t\t<state id="'+outcomes+'" />\n'

    if self.arcConnection != []:
      # print arc
      commentArc = '\t\t\t<!-- add arcs -->\n'
      initArc = '\t\t\t<parents>'
      for i in range(len(self.arcConnection)):
        initArc += self.arcConnection[i][0]+' '
      endArc =  '</parents>\n'
    else:
      commentArc = ''
      initArc = ''
      endArc = ''

    endNode = '\t\t</decision>\n'
    print_node =  commentNode+initNode+commentOutcomes+initOutcomes+commentArc+initArc+endArc+endNode
    return print_node

class Utility(Node):
  """Utility element for the Bayesian Network

  :Attributes:
    - name (str): Name of the node
  """

  def __init__(self, name):
    self.name = name
    Node.__init__(self,name)


  def setUtilities(self,utilities):
    """Set the utilities for the node

    The order of these utilities is given by considering the state of the
    first parent of the node as the most significant coordinate, then the
    second parent, then the third (and so on), and finally considering the
    coordinate of the node itself as the least significant one.

    :Args:
      - utilities (list): A list of utilities for the node
    """
    self.probabilities = utilities


  def printNode(self):
    # print node
    commentNode = '\t\t<!-- create utility "'+self.caption+'" -->\n'
    initNode = '\t\t<utility id="'+self.name+'" >\n'

    if self.arcConnection != []:
      # print arc
      commentArc = '\t\t\t<!-- add arcs -->\n'
      initArc = '\t\t\t<parents>'
      for i in range(len(self.arcConnection)):
        initArc += self.arcConnection[i][0]+' '
      endArc =  '</parents>\n'
    else:
      commentArc = ''
      initArc = ''
      endArc = ''

    # print probabilities
    commentUtilities = '\t\t\t<!-- setting utilities -->\n'
    initUtilities = '\t\t\t<utilities>'
    for i,probability in enumerate(self.probabilities):
      initUtilities += str(probability)+' '
    endUtilities = '</utilities>\n'
    endNode = '\t\t</utility>\n'
    print_node =  commentNode+initNode+commentArc+initArc+endArc+commentUtilities+initUtilities+endUtilities+endNode
    return print_node


def repEmptySpace(string):
  return string.replace(' ', '_')

