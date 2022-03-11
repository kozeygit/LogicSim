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
    
    def connectGate(self, gate1, gate2):
        if gate1.connectNode(gate2, 1):
            return True
        if gate2.getGateType() != "not" or gate2.getGateType() != "output":
            if gate1.connectNode(gate2, 2):
                return True
        return False
        
    def disconnectGate(self, gate1, gate2):
        return gate1.disconnectNode(gate2)
    
    def getTruthTable(self, gate):
        return generateTruthTable(gate.getExpression())

    def clearBoard(self):
        for i in self.gates[:]:
            print(len(self.gates))
            self.removeGate(i)