
class BinaryTree:
    def __init__(self):
        nodes = []
        root_node = None

class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
# Compare the new value with the parent node
        if self.data:
            if self.left is None:
                self.left = Node(data)
            else:
                self.left.insert(data)
            if self.right is None:
                self.right = Node(data)
            else:
                self.right.insert(data)
        else:
            self.data = data

    def remove(self, data):
        if self.left is data:
            self.left = None
        elif self.right is data:
            self.right = None

# print the tree
    def printTreeInOrder(self):
        if self.left:
            self.left.printTreeInOrder()
        print( self.data),
        if self.right:
            self.right.printTreeInOrder()

    def printTreePreOrder(self):
        if self.left:
            self.left.printTreePreOrder()
        print( self.data),
        if self.right:
            self.right.printTreePreOrder()
    
    def printTreePostOrder(self):
        if self.left:
            self.left.printTreePostOrder()
        print( self.data),
        if self.right:
            self.right.printTreePostOrder()