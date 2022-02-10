from truth_table import *

class Board:
    ID = 0
    def __init__(self):
        self.id = Board.ID
        Board.ID += 1
        self.inputs = []
        self.gates = []
        self.outputs = []
        self.gateStack = None
        self.visitedGatesInParse = []
    
    def addGate(self, gate_type, gate):
        self.gates.append(gate)
    
    def removeGate(self, gate_type, gate_id):
        self.gates.pop(gate_id)
    
    def connectGate(self, gate1_type, gate1_id, gate2_type, gate2_id):
        gate1 = self.checkWhichListGateIn(gate1_type)[gate1_id]
        gate2 = self.checkWhichListGateIn(gate2_type)[gate2_id]
        
    
    def disconnectGate(self, gate1_id, gate2_id):
        pass
    
    def checkWhichListGateIn(self, gate_type):
        gate_lists = {
            'gate':self.gates,
            'input':self.inputs,
            'output':self.output
        }
        gate_type = gate_type.lower()
        return gate_lists[gate_type]

    def getTruthTable(self, gate):
        pass

    def clearBoard(self):
        self.inputs = []
        self.gates = []
        self.outputs = []
    
    def getGate(self, gate_id):
        pass

    def save(self):
        

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

