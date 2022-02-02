import time
from truth_table import *

class Gate: #Logic gates parent class
    ID = 0
    def __init__(self):
        self._input_node1 = False
        self._input_node2 = False
        self._output_nodes = []
        self._output = 0
        self._operator = None
        self._type = ''
        self.expression = None
        
        self.id = Gate.ID
        Gate.ID += 1

    def hasInputs(self):
        return self._input_node1 and self._input_node2
    
    def evaluate(self):
        return

    def updateExpression(self):
        if self.hasInputs():
            if self._input_node1.getGateType() == 'switch':
                exp1 = self._input_node1.getExpression()
            else:
                exp1 = f"({self._input_node1.getExpression()})"
            
            if self._input_node2.getGateType() == 'switch':
                exp2 = self._input_node2.getExpression()
            else:
                exp2 = f"({self._input_node2.getExpression()})"
            
            self.expression = f"{exp1} {self._type} {exp2}"
        else:
            self.expression = None

    def getExpression(self):
        return self.expression


  # Rewrite, doesnt handle flip flop recursion
    def _process(self):
        if self.hasInputs():
            var1 = self._input_node1.getOutput()
            var2 = self._input_node2.getOutput()
            self._output = self.evaluate(var1, var2)
        else:
            print("Gate is missing input(s)")
            print(self._input_node1)
            print(self._input_node2)

    def getGateType(self):
        return self._type

    def getOutput(self):
        self._process()
        return self._output

    def connectNode(self, node, gate):
        if node == 1:
            if self._input_node1 == False:
                self._input_node1 = gate
                gate.connectNode(-1, self)
                self.updateExpression()
            else:
                print(f"{self.name}\nConnected to another node already")
        elif node == 2:
            if self._input_node2 == False:
                self._input_node2 = gate
                gate.connectNode(-1, self)
                self.updateExpression()
            else:
                print(f"{self.name}\nConnected to another node already")
        elif node == -1:
            self._output_nodes.append(gate)

    def disconnectNode(self, node, gate):
        if node == 1:
            self._input_node1.disconnectNode(-1, self)
            self._input_node1 = False
            self.updateExpression()
        elif node == 2:
            self._input_node1.disconnectNode(-1, self)
            self._input_node2 = False
            self.updateExpression()
        elif node == -1:
            self._output_nodes.remove(gate)



class And_Gate(Gate):
    def __init__(self):
        super().__init__()
        self._operator = '&'
        self._type = 'and'
        self.name = f"{self._type}_{str(self.id)}"
        

    def evaluate(self, var1, var2):
        return (var1 and var2)


class Or_Gate(Gate):
    def __init__(self):
        super().__init__()
        self._operator = '|'
        self._type = 'or'
        self.name = f"{self._type}_{str(self.id)}"

    def evaluate(self, var1, var2):
        return (var1 or var2)

class Xor_Gate(Gate):
    def __init__(self):
        super().__init__()
        self._operator = '^'
        self._type = 'xor'
        self.name = f"{self._type}_{str(self.id)}"

    def evaluate(self, var1, var2):
        return (var1 and not var2) or (not var1 and var2)

class Not_Gate(Gate):
    def __init__(self):
        super().__init__()
        self._operator = '2+~'
        self._type = 'not'
        self.name = f"{self._type}_{str(self.id)}"

    def hasInputs(self):
        return self._input_node1

    def evaluate(self, var1):
        return int((not var1))

  # Rewrite, doesnt handle flip flop recursion
    def _process(self):
        var1 = self._input_node1.getOutput()
        self._output = self.evaluate(var1)
    
    def connectNode(self, node, gate):
        if node == 1:
            if self._input_node1 == False:
                self._input_node1 = gate
                gate.connectNode(-1, self)
                self.updateExpression()
            else:
                print(f"{self.name}\nConnected to another node already")
        elif node == -1:
            self._output_nodes.append(gate)
  
    def disconnectNode(self, node, gate):
        if node == 1:
            self._input_node1.disconnectNode(-1, self)
            self._input_node1 = False
            self.updateExpression()
        elif node == -1:
            self._output_nodes.remove(gate)

    def updateExpression(self):
        self.expression = str(f"{self._type}({self._input_node1.getExpression()})")


class Switch:
    ID = 97
    def __init__(self):
        self._output = 0
        self._output_nodes = []
        self._type = 'switch'
        self.id = chr(Switch.ID)
        Switch.ID += 1
        self.name = (f"{self._type}_{self.id}")
    
    def getGateType(self):
        return self._type
        
    def getExpression(self):
        return self.id

    def getOutput(self):
        return self._output

    def connectNode(self, node, gate):
        if node == -1:
            self._output_nodes.append(gate)

    def disconnectNode(self, node, gate):
        if node == -1:
            self._output_nodes.remove(gate)

    def flip(self):
        self._output = self._output ^ 1

class Output:
    ID = 65
    def __init__(self):
        self._output = 0
        self._input_node = None
        self.id = chr(Output.ID)
        Output.ID += 1
        self.name = (f"output_{self.id}")

    def _process(self):
        try:
            self._output = self._input_node.getOutput()
        except AttributeError:
            self._output = -1
  
    def getExpression(self):
        return self._input_node.getExpression()

    def connectNode(self, gate):
        self._input_node = gate
        gate.connectNode(-1, self)

    def truthTable(self):
        generateTruthTable(self.getExpression())


    def getOutput(self):
        self._process()
        return self._output

    def printOutput(self):
        out = self.getOutput()
        if out == -1:
            print("No Output; Incorrect Input")
        else:
            print(out)


class Clock:
    def __init__(self):
        self.time = time.time
        self.state = 0
        self.start_time = self.time()
        self.numTicks = 0

    def getOutput(self):
        return self.state
    
    def change_state(self):
        self.state = (self.state + 1) % 2

    def connectNode(self, *args):
        pass


    def tick(self, FPS):
        if (self.time() - self.start_time) >= (1/FPS):
            self.start_time = self.time()
            self.numTicks += 1
            self.change_state()