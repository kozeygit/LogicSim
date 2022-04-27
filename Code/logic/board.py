from logic.gates import *
from logic.truth_table import *

'''Docstrings Done, Not proofread'''

class Board:
    '''Logic Board class.'''
    ID = 0
    def __init__(self) -> None:
        self.id = Board.ID
        Board.ID += 1
        self.gates = []

    def add_gate(self, gate: Gate) -> None:
        '''Adds given component to gate array.'''
        self.gates.append(gate)

    def remove_gate(self, gate: Gate) -> None:
        '''Removes given component from gate array.'''
        gate.disconnect_all()
        self.gates.remove(gate)

    def connect_gate(self, in_gate: Gate, out_gate: Gate, node: int) -> bool:
        '''Connects two given components together'''
        if node == 1:
            if in_gate.connect_node(out_gate, 1):
                return True
        if node == 2:
            if in_gate.get_gate_type() != "not" or in_gate.get_gate_type() != "output":
                if in_gate.connect_node(out_gate, 2):
                    return True
        return False

    def disconnect_gate(self, in_gate: Gate, out_gate: Gate) -> bool:
        '''Disconnects two given components from eachother'''
        return in_gate.disconnect_node(out_gate)

    def clear_board(self) -> None:
        '''Removes all components from gate array'''
        for gate in self.gates[:]:
            self.remove_gate(gate)
