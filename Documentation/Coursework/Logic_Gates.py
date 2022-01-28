class Gate:
  def __init__(self):
    self.input_node1 = None
    self.input_node2 = None
    self.output_node = None
    self.output = None
    self.operator = ''
    
    #self.drag = False

  def getOutput(self):
    self.process()
    return self.output

  def process(self):
    var1 = self.input_node1.getOutput()
    var2 = self.input_node2.getOutput()
    expression = f"{var1} {self.operator} {var2}"
    self.output = eval(expression)
  
  def connectNode(self, node, gate):
    if node == 1:
      if self.input_node1 == None:
        self.input_node1 = gate
        gate.connectNode(-1, self)
      else:
        print("Connected to another node already")
    elif node == 2:
      if self.input_node2 == None:
        self.input_node2 = gate
        gate.connectNode(-1, self)
      else:
        print("Connected to another node already")
    elif node == -1:
      self.output_node = gate

  def disconnectNode(self, node):
    if node == 1:
      self.input_node1 = None
    elif node == 2:
      self.input_node2 = None
  
  # def enableDrag(self, boo):
  #   if boo == 1:
  #     self.drag = True
  #   elif boo == 0:
  #     self.drag = False

class And_Gate(Gate):
  def __init__(self):
    super().__init__()
    self.operator = '&'

class Or_Gate(Gate):
  def __init__(self):
    super().__init__()
    self.operator = '|'

class Xor_Gate(Gate):
  def __init__(self):
    super().__init__()
    self.operator = '^'

class Not_Gate(Gate):
  def __init__(self):
    super().__init__()
    self.operator = '2+~'

  def process(self):
    var1 = self.input_node1.getOutput()
    expression = f"{self.operator}{var1}"
    self.output = eval(expression)
  
  def connectNode(self, node, gate):
    if node == 1:
      if self.input_node1 == None:
        self.input_node1 = gate
        gate.connectNode(-1, self)
      else:
        print("Connected to another node already")
    elif node == -1:
      self.output_node = gate

  def disconnectNode(self, node):
    if node == 1:
      self.input_node1.disconnectNode(-1)
      self.input_node1 = None
    elif node == -1:
      self.output_node = None

  


class Switch:
  def __init__(self):
    self.output = 0
    self.outputNode = None

  def getOutput(self):
    return self.output

  def connectNode(self, node, gate):
    if node == -1:
      self.output_node = gate

  def flip(self):
    self.output = self.output ^ 1