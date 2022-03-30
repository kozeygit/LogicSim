from logic.gates import *
from logic.truth_table import *

class Board:
    ID = 0
    def __init__(self):
        self.id = Board.ID
        Board.ID += 1
        self.gates = []
    
    def addGate(self, *gates):
        for gate in gates:
            self.gates.append(gate)
    
    def removeGate(self, gate):
        gate.disconnectAll()
        self.gates.remove(gate)
    
    def connectGate(self, inGate, outGate, node=0):
        if node == 1:
            if inGate.connectNode(outGate, 1):
                return True
        if node == 2:
            if inGate.getGateType() != "not" or inGate.getGateType() != "output":
                if inGate.connectNode(outGate, 2):
                    return True
        return False

    def disconnectGate(self, gate1, gate2):
        return gate1.disconnectNode(gate2)

    def clearBoard(self):
        for i in self.gates[:]:
            print(len(self.gates))
            self.removeGate(i)