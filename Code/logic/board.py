from logic.gates import *
from logic.truth_table import *


class Board:
    ID = 0

    def __init__(self):
        self.id = Board.ID
        Board.ID += 1
        self.gates = []

    def add_gate(self, *gates):
        for gate in gates:
            self.gates.append(gate)

    def remove_gate(self, gate):
        gate.disconnectAll()
        self.gates.remove(gate)

    def connect_gate(self, in_gate, out_gate, node=0):
        if node == 1:
            if in_gate.connectNode(out_gate, 1):
                return True
        if node == 2:
            if in_gate.getGateType() != "not" or in_gate.getGateType() != "output":
                if in_gate.connectNode(out_gate, 2):
                    return True
        print("DIDNT WORK NO LINE SHOULD APPEAR")
        return False

    def disconnect_gate(self, in_gate, out_gate):
        return in_gate.disconnectNode(out_gate)

    def clear_board(self):
        for i in self.gates[:]:
            self.remove_gate(i)
