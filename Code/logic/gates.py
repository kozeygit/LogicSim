
'''
Gates Vectors Needed: And, Or, Xor, Not, Switch(on, off), Output(on, off)
'''

class Gate: #Logic gates parent class
    '''Logic Gate parent class'''
    ID = 0
    def __init__(self):
        self._input_nodes = [None, None]
        self._output_nodes = []
        self._output = None
        self._type = ''
        self._expression = None
        self.name = ''
        self.id = Gate.ID
        Gate.ID += 1

    def evaluate(self):
        pass
    
    # Returns True if node given is empty, or if no node is given, returns True if both are empty. 
    def hasInput(self, node=0):
        if node == 0:
            return bool(self._input_nodes[0] and self._input_nodes[1])
        elif node == 1:
            return bool(self._input_nodes[0])
        elif node == 2:
            return bool(self._input_nodes[1])

    def connectNode(self, gate, node):
        if gate in self._input_nodes:
            print("Gate connected to me already")
            return False
        if node == 1:
            if not self.hasInput(1):
                self._input_nodes[0] = gate
                gate.connectNode(self, -1)
                self.updateExpression()
                return True
            else:
                print(f"{self.name}\n node 1 Connected to another gate already")
                return False
        elif node == 2:
            if not self.hasInput(2):
                self._input_nodes[1] = gate
                gate.connectNode(self, -1)
                self.updateExpression()
                return True
            else:
                print(f"{self.name}\n node 2 Connected to another gate already")
                return False
        elif node == -1:
            self._output_nodes.append(gate)
            return

    def disconnectNode(self, gate):
        if self._input_nodes[0] is gate:
            self._input_nodes[0].disconnectNode(self)
            self._input_nodes[0] = None
            self.updateExpression()
            return True
        elif self._input_nodes[1] is gate:
            self._input_nodes[1].disconnectNode(self)
            self._input_nodes[1] = None
            self.updateExpression()
            return True
        elif gate in self._output_nodes:
            self._output_nodes.remove(gate)
            return True
        else:
            print(f"No connection between {self.name} and {gate.getName()}")
            return False

    def disconnectAll(self): # Use when deleting gate
        if self._input_nodes[0] != None:
            self._input_nodes[0].disconnectNode(self)
            self._input_nodes[0] = None
            self.updateExpression()
        if self._input_nodes[1] != None:
            self._input_nodes[1].disconnectNode(self)
            self._input_nodes[1] = None
            self.updateExpression()
        for i in self._output_nodes:
            i.disconnectNode(self)
        
    
  # doesnt handle flip flop recursion
    def _process(self):
        if self.hasInput():
            var1 = self._input_nodes[0].getOutput()
            var2 = self._input_nodes[1].getOutput()
            if var1 == None or var2 == None:
                self._output = None
            else:
                self._output = self.evaluate(var1, var2)
        else:
            self._output = None
            print("Gate is missing input(s)")
            print(self._input_nodes[0])
            print(self._input_nodes[1])
    
    def updateExpression(self):
        if self.hasInput():
            if self._input_nodes[0].getGateType() == 'switch':
                exp1 = self._input_nodes[0].getExpression()
            else:
                exp1 = f"({self._input_nodes[0].getExpression()})"
                
            if self._input_nodes[1].getGateType() == 'switch':
                exp2 = self._input_nodes[1].getExpression()
            else:
                exp2 = f"({self._input_nodes[1].getExpression()})"
            
            self._expression = f"{exp1} {self._type} {exp2}"
        else:
            self._expression = None

    def getExpression(self):
        return self._expression

    def getGateType(self):
        return self._type

    def getOutput(self):
        self._process()
        return self._output

    def getName(self):
        return self.name




class And_Gate(Gate):
    
    def __init__(self):
        super().__init__()
        self._type = 'and'
        self.name = f"{self._type}_{str(self.id)}"
        
    def evaluate(self, var1, var2):
        return (var1 and var2)


class Or_Gate(Gate):
    def __init__(self):
        super().__init__()
        self._type = 'or'
        self.name = f"{self._type}_{str(self.id)}"

    def evaluate(self, var1, var2):
        return (var1 or var2)

class Xor_Gate(Gate):
    def __init__(self):
        super().__init__()
        self._type = 'xor'
        self.name = f"{self._type}_{str(self.id)}"

    def evaluate(self, var1, var2):
        return (var1 and not var2) or (not var1 and var2)

class Not_Gate(Gate):
    def __init__(self):
        super().__init__()
        self._type = 'not'
        self.name = f"{self._type}_{str(self.id)}"

    def hasInput(self):
        return bool(self._input_nodes[0])

    def evaluate(self, var1):
        return int((not var1))

  # Rewrite, doesnt handle flip flop recursion
    def _process(self):
        if self.hasInput():
            var1 = self._input_nodes[0].getOutput()
            if var1 == None:
                self._output = None
            else:
                self._output = self.evaluate(var1)
        else:
            self._output = None
    
    def connectNode(self, gate, node):
        if node == 1:
            if not self.hasInput():
                self._input_nodes[0] = gate
                gate.connectNode(self, -1)
                self.updateExpression()
                return True
            else:
                print(f"{self.name}\nConnected to another node already")
                return False
  
    def disconnectNode(self, gate):
        if self._input_nodes[0] is gate:
            self._input_nodes[0].disconnectNode(self)
            self._input_nodes[0] = None
            self.updateExpression()
            return True
        elif gate in self._output_nodes:
            self._output_nodes.remove(gate)
            return True
        else:
            print(f"No connection between {self.name} and {gate.getName()}")
            return False

    def disconnectAll(self): # Use when deleting gate
        if not self._input_nodes[0] == None:
            self._input_nodes[0].disconnectNode(self)
            self._input_nodes[0] = None
            self.updateExpression()

    def updateExpression(self):
        if self.hasInput():
            self._expression = str(f"{self._type}({self._input_nodes[0].getExpression()})")
        else:
            self._expression = None


class Switch:
    ID = 97
    def __init__(self):
        self._output = 0
        self._output_nodes = []
        self._type = 'switch'
        self.id = chr(Switch.ID)
        Switch.ID += 1
        self.name = (f"{self._type}_{self.id}")
 
    def connectNode(self, gate, node):
        if gate not in self._output_nodes:
            self._output_nodes.append(gate)
            return True
        return False

    def disconnectNode(self, gate):
        if gate in self._output_nodes:
            self._output_nodes.remove(gate)
            return True
        return False

    def disconnectAll(self):
        for gate in self._output_nodes:
            gate.disconnectNode(self)

    def flip(self):
        self._output = int(not(self._output))
        #print(self._output_nodes)

    def getName(self):
        return self.name
    
    def getGateType(self):
        return self._type
        
    def getExpression(self):
        return self.id

    def getOutput(self):
        return self._output

class Output:
    ID = 65
    def __init__(self):
        self._output = None
        self._input_nodes = [None]
        self._type = 'output'
        self.id = chr(Output.ID)
        Output.ID += 1
        self.name = (f"{self._type}_{self.id}")

    def _process(self):
        try:
            self._output = self._input_nodes[0].getOutput()
        except AttributeError as e:
            print(e, len(self._input_nodes))
            self._output = None
  
    def connectNode(self, gate, node):
        if self._input_nodes[0] == None:
            self._input_nodes[0] = gate
            gate.connectNode(self, -1)
            return True
        else:
            print("Node already connected to", self._input_nodes[0])
            return False

    def disconnectNode(self, gate):
        if self._input_nodes[0] is gate:
            self._input_nodes[0] = None
            gate.disconnectNode(self)
            return True
        return False

    def disconnectAll(self):
        if self._input_nodes[0] == None:
            pass
        else:
            self._input_nodes[0].disconnectNode(self)
            self._input_nodes[0] = None
        self._process()

    def getExpression(self):
        return self._input_nodes[0].getExpression()

    def getName(self):
        return self.name

    def getGateType(self):
        return self._type

    def getOutput(self):
        self._process()
        return self._output

