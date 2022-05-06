'''
Docstrings Done, not proof read.
'''

from typing import Union # For type hinting

class Gate:
    '''Logic Gate component class. Parent class for logic gates.'''
    ID = 0
    def __init__(self) -> None:
        self._input_nodes = [None, None]
        self._output_nodes = []
        self._output = None
        self._type = ''
        self._expression = None
        self.name = ''
        self.id = Gate.ID
        Gate.ID += 1

    def evaluate(self) -> None:
        '''Not implemented in parent class.'''
        pass
    
    def has_input(self, node=0) -> bool:
        '''Checks if nodes are connected to other components.'''
        if node == 0:
            return bool(self._input_nodes[0] and self._input_nodes[1])
        elif node == 1:
            return bool(self._input_nodes[0])
        elif node == 2:
            return bool(self._input_nodes[1])

    def connect_node(self, gate, node) -> bool:
        '''Connects given component to given node of self'''
        if gate in self._input_nodes:
            return False
        if node == 1:
            if not self.has_input(1):
                self._input_nodes[0] = gate
                gate.connect_node(self, -1)
                self.update_expression()
                return True
            else:
                return False
        elif node == 2:
            if not self.has_input(2):
                self._input_nodes[1] = gate
                gate.connect_node(self, -1)
                self.update_expression()
                return True
            else:
                return False
        elif node == -1:
            self._output_nodes.append(gate)
            return True

    def disconnect_node(self, gate) -> bool:
        '''Disconnects given component from self.'''
        if self._input_nodes[0] is gate:
            self._input_nodes[0].disconnect_node(self)
            self._input_nodes[0] = None
            self.update_expression()
            return True
        elif self._input_nodes[1] is gate:
            self._input_nodes[1].disconnect_node(self)
            self._input_nodes[1] = None
            self.update_expression()
            return True
        elif gate in self._output_nodes:
            self._output_nodes.remove(gate)
            return True
        else:
            return False

    def disconnect_all(self) -> None:
        '''Disconnects all inputs and outputs from self.'''
        if self._input_nodes[0] != None:
            self._input_nodes[0].disconnect_node(self)
            self._input_nodes[0] = None
            self.update_expression()
        if self._input_nodes[1] != None:
            self._input_nodes[1].disconnect_node(self)
            self._input_nodes[1] = None
            self.update_expression()
        for gate in self._output_nodes:
            gate.disconnect_node(self)
        
    def _process(self) -> None:
        '''Uses evaluate method to set output of self. If both input nodes empty, or any input nodes output is None, output is set to None.'''
        if self.has_input():
            var1 = self._input_nodes[0].get_output()
            var2 = self._input_nodes[1].get_output()
            if var1 == None or var2 == None:
                self._output = None
            else:
                self._output = self.evaluate(var1, var2)
        else:
            self._output = None
    
    def update_expression(self) -> None:
        '''Updates the boolean expression of self. Used when connecting or disconnecting components to/from self.'''
        if self.has_input():
            if self._input_nodes[0].get_gate_type() == 'switch':
                exp1 = self._input_nodes[0].get_expression()
            else:
                exp1 = f"({self._input_nodes[0].get_expression()})"
            if self._input_nodes[1].get_gate_type() == 'switch':
                exp2 = self._input_nodes[1].get_expression()
            else:
                exp2 = f"({self._input_nodes[1].get_expression()})"
            
            self._expression = f"{exp1} {self._type} {exp2}"
        else:
            self._expression = None

    def get_expression(self) -> str:
        '''Returns boolean expression of self.'''
        return self._expression

    def get_gate_type(self) -> str:
        '''Returns the type of component that self is.'''
        return self._type

    def get_name(self) -> str:
        '''Returns the name of self. Name is string: type_id.'''
        return self.name
    
    def get_output(self) -> Union[int, None]:
        '''Calls process method, then return output of self.'''
        self._process()
        return self._output


class And_Gate(Gate):
    '''Logic And_Gate component class, child of Gate class.'''
    def __init__(self) -> None:
        super().__init__()
        self._type = 'and'
        self.name = f"{self._type}_{str(self.id)}"
        
    def evaluate(self, var1, var2) -> int:
        '''Return the result of an and comparison bewtween two variables.'''
        return int(var1 and var2)


class Or_Gate(Gate):
    '''Logic Or_Gate component class, child of Gate class.'''
    def __init__(self) -> None:
        super().__init__()
        self._type = 'or'
        self.name = f"{self._type}_{str(self.id)}"

    def evaluate(self, var1, var2) -> int:
        '''Return the result of an or comparison bewtween two variables.'''
        return int(var1 or var2)


class Xor_Gate(Gate):
    '''Logic Xor_Gate component class, child of Gate class.'''
    def __init__(self) -> None:
        super().__init__()
        self._type = 'xor'
        self.name = f"{self._type}_{str(self.id)}"

    def evaluate(self, var1, var2) -> int:
        '''Return the result of an xor comparison bewtween two variables.'''
        return int((var1 and not var2) or (not var1 and var2))


class Not_Gate(Gate):
    '''Logic Not_Gate component class, child of Gate class.'''
    def __init__(self) -> None:
        super().__init__()
        self._type = 'not'
        self.name = f"{self._type}_{str(self.id)}"

    def evaluate(self, var1) -> int:
        '''Return the result of a not operation on a variable.'''
        return int((not var1))
    
    def has_input(self) -> bool:
        '''Checks if input node is connected to another component.'''
        return bool(self._input_nodes[0])

    def _process(self) -> None:
        '''Uses evaluate method to set output of self. If has no input node, or input nodes output is None, output is set to None.'''
        if self.has_input():
            var1 = self._input_nodes[0].get_output()
            if var1 == None:
                self._output = None
            else:
                self._output = self.evaluate(var1)
        else:
            self._output = None
    
    def connect_node(self, gate, node) -> bool:
        '''Connects given component to given node of self.'''
        if gate in self._input_nodes:
            return False
        if node == 1:
            if not self.has_input():
                self._input_nodes[0] = gate
                gate.connect_node(self, -1)
                self.update_expression()
                return True
            else:
                return False
        elif node == -1:
            self._output_nodes.append(gate)
            return True
  
    def disconnect_node(self, gate) -> bool:
        '''Disconnects given component from self.'''
        if self._input_nodes[0] is gate:
            self._input_nodes[0].disconnect_node(self)
            self._input_nodes[0] = None
            self.update_expression()
            return True
        elif gate in self._output_nodes:
            self._output_nodes.remove(gate)
            return True
        else:
            return False

    def disconnect_all(self) -> None:
        '''Disconnects all inputs and outputs from self.'''
        if self._input_nodes[0] != None:
            self._input_nodes[0].disconnect_node(self)
            self._input_nodes[0] = None
            self.update_expression()
        for gate in self._output_nodes:
            gate.disconnect_node(self)

    def update_expression(self) -> None:
        '''Updates the boolean expression of self. Used when connecting or disconnecting components to/from self.'''
        if self.has_input():
            self._expression = str(f"{self._type}({self._input_nodes[0].get_expression()})")
        else:
            self._expression = None


class Switch:
    '''Logic Switch component class.'''
    ID = 0
    def __init__(self) -> None:
        self._output = 0
        self._output_nodes = []
        self._type = 'switch'
        self.id = chr(Switch.ID+97)
        Switch.ID += 1
        self.name = (f"{self._type}_{self.id}")
 
    def connect_node(self, gate, node) -> bool:
        '''Connects given component to given node of self.'''
        if gate not in self._output_nodes and node == -1:
            self._output_nodes.append(gate)
            return True
        return False

    def disconnect_node(self, gate) -> bool:
        '''Disconnects given component from self.'''
        if gate in self._output_nodes:
            self._output_nodes.remove(gate)
            return True
        return False

    def disconnect_all(self) -> None:
        '''Disconnects all inputs and outputs from self.'''
        for gate in self._output_nodes:
            gate.disconnect_node(self)

    def flip(self) -> None:
        '''Changes output of self from 0 to 1 or 1 to 0.'''
        self._output = int(not(self._output))

    def get_name(self) -> str:
        '''Returns the name of self. Name is string: type_id.'''
        return self.name
    
    def get_gate_type(self) -> str:
        '''Returns the type of self that self is.'''
        return self._type
        
    def get_expression(self) -> str:
        '''Return character id of self.'''
        return self.id

    def get_output(self) -> Union[int, None]:
        '''Returns output of self.'''
        return self._output


class Output:
    '''Logic Output component class.'''
    ID = 65
    def __init__(self) -> None:
        self._output = None
        self._input_nodes = [None]
        self._type = 'output'
        self.id = chr(Output.ID)
        Output.ID += 1
        self.name = (f"{self._type}_{self.id}")

    def _process(self) -> None:
        '''Sets output of self to output of input node. If input node is empty, output is set to None.'''
        try:
            self._output = self._input_nodes[0].get_output()
        except AttributeError as e:
            self._output = None
  
    def connect_node(self, gate, node) -> bool:
        '''Connects given component to given node of self.'''
        if self._input_nodes[0] == None:
            self._input_nodes[0] = gate
            gate.connect_node(self, -1)
            return True
        else:
            return False

    def disconnect_node(self, gate) -> bool:
        '''Disconnects given component from self.'''
        if self._input_nodes[0] is gate:
            self._input_nodes[0] = None
            gate.disconnect_node(self)
            return True
        return False

    def disconnect_all(self) -> None:
        '''Disconnects all inputs and outputs from self.'''
        if self._input_nodes[0] == None:
            pass
        else:
            self._input_nodes[0].disconnect_node(self)
            self._input_nodes[0] = None
        self._process()

    def get_expression(self) -> str:
        '''Return boolean expression of input component.'''
        return self._input_nodes[0].get_expression()

    def get_name(self) -> str:
        '''Returns the name of self. Name is string: type_id.'''
        return self.name

    def get_gate_type(self) -> str:
        '''Returns the type of component that self is.'''
        return self._type

    def get_output(self) -> Union[int, None]:
        '''Calls process method, then return output of self.'''
        self._process()
        return self._output

