'''
Docstrings Done, not proof read.
'''

class Gate:
    '''Logic Gate component class. Parent class for logic gates.'''
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
        '''Not implemented in parent class.'''
        pass
    
    def hasInput(self, node=0):
        '''Checks if nodes are connected to other components.'''
        if node == 0:
            return bool(self._input_nodes[0] and self._input_nodes[1])
        elif node == 1:
            return bool(self._input_nodes[0])
        elif node == 2:
            return bool(self._input_nodes[1])

    def connectNode(self, gate, node):
        '''Connects given component to given node of self'''
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
        '''Disconnects given component from self.'''
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

    def disconnectAll(self):
        '''Disconnects all inputs and outputs from self.'''
        if self._input_nodes[0] != None:
            self._input_nodes[0].disconnectNode(self)
            self._input_nodes[0] = None
            self.updateExpression()
        if self._input_nodes[1] != None:
            self._input_nodes[1].disconnectNode(self)
            self._input_nodes[1] = None
            self.updateExpression()
        for gate in self._output_nodes:
            gate.disconnectNode(self)
        
    def _process(self):
        '''Uses evaluate method to set output of self. If both input nodes empty, or any input nodes output is None, output is set to None.'''
        if self.hasInput():
            var1 = self._input_nodes[0].getOutput()
            var2 = self._input_nodes[1].getOutput()
            if var1 == None or var2 == None:
                self._output = None
            else:
                self._output = self.evaluate(var1, var2)
        else:
            self._output = None
    
    def updateExpression(self):
        '''Updates the boolean expression of self. Used when connecting or disconnecting components to/from self.'''
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
        '''Returns boolean expression of self.'''
        return self._expression

    def getGateType(self):
        '''Returns the type of component that self is.'''
        return self._type

    def getOutput(self):
        '''Calls process method, then return output of self.'''
        self._process()
        return self._output

    def getName(self):
        '''Returns the name of self. Name is string: type_id.'''
        return self.name


class And_Gate(Gate):
    '''Logic And_Gate component class, child of Gate class.'''
    def __init__(self):
        super().__init__()
        self._type = 'and'
        self.name = f"{self._type}_{str(self.id)}"
        
    def evaluate(self, var1, var2):
        '''Return the result of an and comparison bewtween two variables.'''
        return (var1 and var2)


class Or_Gate(Gate):
    '''Logic Or_Gate component class, child of Gate class.'''
    def __init__(self):
        super().__init__()
        self._type = 'or'
        self.name = f"{self._type}_{str(self.id)}"

    def evaluate(self, var1, var2):
        '''Return the result of an or comparison bewtween two variables.'''
        return (var1 or var2)


class Xor_Gate(Gate):
    '''Logic Xor_Gate component class, child of Gate class.'''
    def __init__(self):
        super().__init__()
        self._type = 'xor'
        self.name = f"{self._type}_{str(self.id)}"

    def evaluate(self, var1, var2):
        '''Return the result of an xor comparison bewtween two variables.'''
        return (var1 and not var2) or (not var1 and var2)


class Not_Gate(Gate):
    '''Logic Not_Gate component class, child of Gate class.'''
    def __init__(self):
        super().__init__()
        self._type = 'not'
        self.name = f"{self._type}_{str(self.id)}"

    def evaluate(self, var1):
        '''Return the result of a not operation on a variable.'''
        return int((not var1))
    
    def hasInput(self):
        '''Checks if input node is connected to another component.'''
        return bool(self._input_nodes[0])

    def _process(self):
        '''Uses evaluate method to set output of self. If has no input node, or input nodes output is None, output is set to None.'''
        if self.hasInput():
            var1 = self._input_nodes[0].getOutput()
            if var1 == None:
                self._output = None
            else:
                self._output = self.evaluate(var1)
        else:
            self._output = None
    
    def connectNode(self, gate, node):
        '''Connects given component to given node of self.'''
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
        '''Disconnects given component from self.'''
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

    def disconnectAll(self):
        '''Disconnects all inputs and outputs from self.'''
        if self._input_nodes[0] != None:
            self._input_nodes[0].disconnectNode(self)
            self._input_nodes[0] = None
            self.updateExpression()

    def updateExpression(self):
        '''Updates the boolean expression of self. Used when connecting or disconnecting components to/from self.'''
        if self.hasInput():
            self._expression = str(f"{self._type}({self._input_nodes[0].getExpression()})")
        else:
            self._expression = None


class Switch:
    '''Logic Switch component class.'''
    ID = 0
    def __init__(self):
        self._output = 0
        self._output_nodes = []
        self._type = 'switch'
        self.id = chr(Switch.ID+97)
        Switch.ID += 1
        self.name = (f"{self._type}_{self.id}")
 
    def connectNode(self, gate, node):
        '''Connects given component to given node of self.'''
        if gate not in self._output_nodes and node == -1:
            self._output_nodes.append(gate)
            return True
        return False

    def disconnectNode(self, gate):
        '''Disconnects given component from self.'''
        if gate in self._output_nodes:
            self._output_nodes.remove(gate)
            return True
        return False

    def disconnectAll(self):
        '''Disconnects all inputs and outputs from self.'''
        for gate in self._output_nodes:
            gate.disconnectNode(self)

    def flip(self):
        self._output = int(not(self._output))
        #print(self._output_nodes)

    def getName(self):
        '''Returns the name of self. Name is string: type_id.'''
        return self.name
    
    def getGateType(self):
        '''Returns the type of self that self is.'''
        return self._type
        
    def getExpression(self):
        '''Return character id of self.'''
        return self.id

    def getOutput(self):
        '''Returns output of self.'''
        return self._output


class Output:
    '''Logic Output component class.'''
    ID = 65
    def __init__(self):
        self._output = None
        self._input_nodes = [None]
        self._type = 'output'
        self.id = chr(Output.ID)
        Output.ID += 1
        self.name = (f"{self._type}_{self.id}")

    def _process(self):
        '''Sets output of self to output of input node. If input node is empty, output is set to None.'''
        try:
            self._output = self._input_nodes[0].getOutput()
        except AttributeError as e:
            print(e, len(self._input_nodes))
            self._output = None
  
    def connectNode(self, gate, node):
        '''Connects given component to given node of self.'''
        if self._input_nodes[0] == None:
            self._input_nodes[0] = gate
            gate.connectNode(self, -1)
            return True
        else:
            print("Node already connected to", self._input_nodes[0])
            return False

    def disconnectNode(self, gate):
        '''Disconnects given component from self.'''
        if self._input_nodes[0] is gate:
            self._input_nodes[0] = None
            gate.disconnectNode(self)
            return True
        return False

    def disconnectAll(self):
        '''Disconnects all inputs and outputs from self.'''
        if self._input_nodes[0] == None:
            pass
        else:
            self._input_nodes[0].disconnectNode(self)
            self._input_nodes[0] = None
        self._process()

    def getExpression(self):
        '''Return boolean expression of input component.'''
        return self._input_nodes[0].getExpression()

    def getName(self):
        '''Returns the name of self. Name is string: type_id.'''
        return self.name

    def getGateType(self):
        '''Returns the type of component that self is.'''
        return self._type

    def getOutput(self):
        '''Calls process method, then return output of self.'''
        self._process()
        return self._output

