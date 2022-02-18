from logic.gates import *
from logic.truth_table import *



class Board:
    ID = 0
    def __init__(self):
        self.id = Board.ID
        Board.ID += 1
        self.gates = []
        self.gateStack = None
        self.visitedGatesInParse = []
    
    def addGate(self, *gates):
        for gate in gates:
            self.gates.append(gate)
    
    def removeGate(self, gate):
        gate.disconnect
        self.gates.remove(gate)
    
    def connectGate(self, gate1, gate2):
        if gate1.connectNode(gate2, 1):
            return True
        if gate2._type != "not" or gate2._type != "output":
            if gate1.connectNode(gate2, 2):
                return True
        return False
        
    
    def disconnectGate(self, gate1, gate2):
        gate1.disconnectNode(gate2)
    

    def getTruthTable(self, gate):
        return generateTruthTable(gate.getExpression())

    def clearBoard(self):
        self.inputs = []
        self.gates = []
        self.outputs = []
    
    def getGate(self, gate_id):
        pass

    def save(self):
        pass

class Tree:
    def __init__(self):
        self.nodes = []
        self.root = None

    def addNode(self, ):
        node = Node()
        self.nodes.append(node)
    
class Node:
    def __init__(self):
        self.data = None
        self.left = None
        self.right = None

