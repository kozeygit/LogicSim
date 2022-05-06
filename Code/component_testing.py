from pyparsing import And
from logic.gates import *
from logic.board import *
from logic.truth_table import generate_truth_table
import unittest

class TestCreatingComponents(unittest.TestCase):
    '''Test: When components are made they are of the correct type and have empty outputs and inputs.'''
    def test_and(self):
        and_gate = And_Gate()
        self.assertIsInstance(and_gate, And_Gate)
        self.assertIsInstance(and_gate, Gate)
        self.assertListEqual(and_gate._input_nodes, [None, None])
        self.assertListEqual(and_gate._output_nodes, [])
        self.assertEqual(and_gate.get_output(), None)

    def test_or(self):
        or_gate = Or_Gate()
        self.assertIsInstance(or_gate, Or_Gate)
        self.assertIsInstance(or_gate, Gate)
        self.assertListEqual(or_gate._input_nodes, [None, None])
        self.assertListEqual(or_gate._output_nodes, [])
        self.assertEqual(or_gate.get_output(), None)
    
    def test_xor(self):
        xor_gate = Xor_Gate()
        self.assertIsInstance(xor_gate, Xor_Gate)
        self.assertIsInstance(xor_gate, Gate)
        self.assertListEqual(xor_gate._input_nodes, [None, None])
        self.assertListEqual(xor_gate._output_nodes, [])
        self.assertEqual(xor_gate.get_output(), None)
    
    def test_not(self):
        not_gate = Not_Gate()
        self.assertIsInstance(not_gate, Not_Gate)
        self.assertIsInstance(not_gate, Gate)
        self.assertListEqual(not_gate._input_nodes, [None, None])
        self.assertListEqual(not_gate._output_nodes, [])
        self.assertEqual(not_gate.get_output(), None)
    
    def test_switch(self):
        switch = Switch()
        self.assertIsInstance(switch, Switch)
        self.assertListEqual(switch._output_nodes, [])
        self.assertEqual(switch.get_output(), 0)
        switch.flip()
        self.assertEqual(switch.get_output(), 1)
        
    def test_output(self):
        output = Output()
        self.assertIsInstance(output, Output)
        self.assertListEqual(output._input_nodes, [None])
        self.assertEqual(output.get_output(), None)
        

class TestGateEvaluateMethods(unittest.TestCase):
    '''Test: The evaluate methods of each gate returns the correct result.'''
    def test_and(self):
        and_gate = And_Gate()
        self.assertEqual(and_gate.evaluate(0,0), 0)
        self.assertEqual(and_gate.evaluate(0,1), 0)
        self.assertEqual(and_gate.evaluate(1,0), 0)
        self.assertEqual(and_gate.evaluate(1,1), 1)

    def test_or(self):
        or_gate = Or_Gate()
        self.assertEqual(or_gate.evaluate(0,0), 0)
        self.assertEqual(or_gate.evaluate(0,1), 1)
        self.assertEqual(or_gate.evaluate(1,0), 1)
        self.assertEqual(or_gate.evaluate(1,1), 1)
    
    def test_xor(self):
        xor_gate = Xor_Gate()
        self.assertEqual(xor_gate.evaluate(0,0), 0)
        self.assertEqual(xor_gate.evaluate(0,1), 1)
        self.assertEqual(xor_gate.evaluate(1,0), 1)
        self.assertEqual(xor_gate.evaluate(1,1), 0)
    
    def test_not(self):
        not_gate = Not_Gate()
        self.assertEqual(not_gate.evaluate(0), 1)
        self.assertEqual(not_gate.evaluate(1), 0)
                

class TestLogicBoard(unittest.TestCase):
    '''Test: The logic board correctly initiallises, adds, and removes components from its gates array'''
    def setUp(self):
        self.board = Board()
        self.and_gate = And_Gate()
        self.or_gate = Or_Gate()
        self.xor_gate = Xor_Gate()
        self.not_gate = Not_Gate()
        self.switch1 = Switch()
        self.switch2 = Switch()
        self.output = Output()
        
    def add_components_to_board(self):
        self.board.add_gate(self.and_gate)
        self.board.add_gate(self.or_gate)
        self.board.add_gate(self.xor_gate)
        self.board.add_gate(self.not_gate)
        self.board.add_gate(self.switch1)
        self.board.add_gate(self.switch2)
        self.board.add_gate(self.output)
        
    def test_board_initially_empty(self):
        self.assertListEqual(self.board.gates, [])
        
    def test_adding_components(self):
        self.add_components_to_board()
        self.assertListEqual(self.board.gates, [self.and_gate, self.or_gate, self.xor_gate, self.not_gate, self.switch1, self.switch2, self.output])
        
    def test_removing_components(self):
        self.board.add_gate(self.switch1)
        self.board.add_gate(self.switch2)
        self.board.add_gate(self.output)
        self.assertListEqual(self.board.gates, [self.switch1, self.switch2, self.output])
        self.board.remove_gate(self.switch2)
        self.assertListEqual(self.board.gates, [self.switch1, self.output])
    
class TestConnectingComponents(unittest.TestCase):
    '''Test: The logic board correctly connects components.'''
    def setUp(self):
        self.board = Board()
        self.and_gate = And_Gate()
        self.switch1 = Switch()
        self.switch2 = Switch()
        
    def add_components_to_board(self):
        self.board.add_gate(self.and_gate)
        self.board.add_gate(self.switch1)
        self.board.add_gate(self.switch2)
    
    def test_connecting_components(self):
        self.add_components_to_board()
        self.board.connect_gate(self.and_gate, self.switch1, 1)
        self.board.connect_gate(self.and_gate, self.switch2, 2)
        self.assertListEqual(self.and_gate._input_nodes, [self.switch1, self.switch2])
        self.assertIn(self.and_gate, self.switch1._output_nodes)
             
        
class TestDisconnectingComponents(unittest.TestCase):
    '''Test: The logic board correctly disconnects components.'''
    def setUp(self):
        self.board = Board()
        self.and_gate = And_Gate()
        self.switch1 = Switch()
        self.switch2 = Switch()
        
    def add_components_to_board(self):
        self.board.add_gate(self.and_gate)
        self.board.add_gate(self.switch1)
        self.board.add_gate(self.switch2)
    
    def test_disconnecting_two_input_components(self):
        self.add_components_to_board()
        self.board.connect_gate(self.and_gate, self.switch1, 1)
        self.board.connect_gate(self.and_gate, self.switch2, 2)
        self.board.disconnect_gate(self.and_gate, self.switch1)
        self.assertListEqual(self.and_gate._input_nodes, [None, self.switch2])
    
class TestRemovingComponentsWithConnections(unittest.TestCase):
    '''Test: The logic board disconnects everything from a component it is removing.'''
    def setUp(self):
        self.board = Board()
        self.xor_gate = Xor_Gate()
        self.switch1 = Switch()
        self.switch2 = Switch()
        self.output = Output()
        
    def add_components_to_board(self):
        self.board.add_gate(self.xor_gate)
        self.board.add_gate(self.switch1)
        self.board.add_gate(self.switch2)
        self.board.add_gate(self.output)
    
    def test_removing_component_with_connections(self):
        self.add_components_to_board()
        self.board.connect_gate(self.xor_gate, self.switch1, 1)
        self.board.connect_gate(self.xor_gate, self.switch2, 2)
        self.board.connect_gate(self.output, self.xor_gate, 1)
        
        self.assertListEqual(self.xor_gate._input_nodes, [self.switch1, self.switch2])
        self.assertListEqual(self.switch1._output_nodes, [self.xor_gate])
        self.assertListEqual(self.switch2._output_nodes, [self.xor_gate])
        
        self.assertListEqual(self.xor_gate._output_nodes, [self.output])
        self.assertListEqual(self.output._input_nodes, [self.xor_gate])
        
        self.assertIn(self.xor_gate, self.board.gates)
        self.board.remove_gate(self.xor_gate)
        self.assertListEqual(self.xor_gate._input_nodes, [None, None])
        self.assertListEqual(self.switch1._output_nodes, [])
        self.assertListEqual(self.switch2._output_nodes, [])
        
        self.assertListEqual(self.xor_gate._output_nodes, [])
        self.assertListEqual(self.output._input_nodes, [None])
        
class TestComponentExpressions(unittest.TestCase):
    '''Test: The expression update correctly'''
    def setUp(self):
        self.board = Board()
        self.and_gate = And_Gate()
        self.or_gate = Or_Gate()
        self.not_gate = Not_Gate()
        self.switch1 = Switch()
        self.switch2 = Switch()
        self.output = Output()
        
    def test_expression_none_when_no_input(self):
        expression = self.and_gate.get_expression()
        self.assertEqual(expression, None)
        
    def test_with_not_enough_inputs(self):
        self.board.connect_gate(self.and_gate, self.switch1, 1)
        expression = self.and_gate.get_expression()
        self.assertEqual(expression, None)
        
    def test_with_inputs_that_have_no_expression(self):
        self.board.connect_gate(self.and_gate, self.or_gate, 1)
        self.board.connect_gate(self.and_gate, self.not_gate, 2)
        expression = self.and_gate.get_expression()
        self.assertEqual(expression, None)
        
    def test_with_valid_inputs(self):
        self.board.connect_gate(self.and_gate, self.switch1, 1)
        self.board.connect_gate(self.and_gate, self.switch2, 2)
        switch_variable1 = self.switch1.get_expression()
        switch_variable2 = self.switch2.get_expression()
        expression = self.and_gate.get_expression()
        valid_expression = f"{switch_variable1} and {switch_variable2}"
        self.assertEqual(expression, valid_expression)
        
    def test_expression_set_to_none_when_inputs_removed(self):
        self.board.connect_gate(self.and_gate, self.switch1, 1)
        self.board.connect_gate(self.and_gate, self.switch2, 2)
        switch_variable1 = self.switch1.get_expression()
        switch_variable2 = self.switch2.get_expression()
        expression1 = self.and_gate.get_expression()
        valid_expression = f"{switch_variable1} and {switch_variable2}"
        self.assertEqual(expression1, valid_expression)
        self.board.disconnect_gate(self.and_gate, self.switch1)
        self.board.disconnect_gate(self.and_gate, self.switch2)
        expression2 = self.and_gate.get_expression()
        self.assertNotEqual(expression2, valid_expression)
        self.assertEqual(expression2, None)
        
class TestStatesCorrectlyChange(unittest.TestCase):
    '''Test: The states of components update correctly when an input is altered.'''
    def setUp(self):
        self.board = Board()
        self.and_gate = And_Gate()
        self.or_gate = Or_Gate()
        self.xor_gate = Xor_Gate()
        self.not_gate = Not_Gate()
        self.switch1 = Switch()
        self.switch2 = Switch()
        self.output = Output()
        
        self.board.add_gate(self.and_gate)
        self.board.add_gate(self.or_gate)
        self.board.add_gate(self.xor_gate)
        self.board.add_gate(self.not_gate)
        self.board.add_gate(self.switch1)
        self.board.add_gate(self.switch2)
        self.board.add_gate(self.output)
        
    def test_and(self):
        self.board.connect_gate(self.and_gate, self.switch1, 1)
        self.board.connect_gate(self.and_gate, self.switch2, 2)
        self.assertEqual(self.and_gate.get_output(), 0) #[0,0] -> 0
        self.switch1.flip()
        self.assertEqual(self.and_gate.get_output(), 0) #[1,0] -> 0
        self.switch1.flip()
        self.switch2.flip()
        self.assertEqual(self.and_gate.get_output(), 0) #[0,1] -> 0
        self.switch1.flip()
        self.assertEqual(self.and_gate.get_output(), 1) #[1,1] -> 1
    
    def test_or(self):
        self.board.connect_gate(self.or_gate, self.switch1, 1)
        self.board.connect_gate(self.or_gate, self.switch2, 2)
        self.assertEqual(self.or_gate.get_output(), 0) #[0,0] -> 0
        self.switch1.flip()
        self.assertEqual(self.or_gate.get_output(), 1) #[1,0] -> 1
        self.switch1.flip()
        self.switch2.flip()
        self.assertEqual(self.or_gate.get_output(), 1) #[0,1] -> 1
        self.switch1.flip()
        self.assertEqual(self.or_gate.get_output(), 1) #[1,1] -> 1
    
    def test_xor(self):
        self.board.connect_gate(self.xor_gate, self.switch1, 1)
        self.board.connect_gate(self.xor_gate, self.switch2, 2)
        self.assertEqual(self.xor_gate.get_output(), 0) #[0,0] -> 0
        self.switch1.flip()
        self.assertEqual(self.xor_gate.get_output(), 1) #[1,0] -> 1
        self.switch1.flip()
        self.switch2.flip()
        self.assertEqual(self.xor_gate.get_output(), 1) #[0,1] -> 1
        self.switch1.flip()
        self.assertEqual(self.xor_gate.get_output(), 0) #[1,1] -> 0
    
    def test_not(self):
        self.board.connect_gate(self.not_gate, self.switch1, 1)
        self.assertEqual(self.not_gate.get_output(), 1) #[0] -> 1
        self.switch1.flip()
        self.assertEqual(self.not_gate.get_output(), 0) #[1] -> 0
    
    def test_output(self):
        self.board.connect_gate(self.output, self.switch1, 1)
        self.assertEqual(self.output.get_output(), 0) #[0] -> 0
        self.switch1.flip()
        self.assertEqual(self.output.get_output(), 1) #[1] -> 1
    
class TestTruthTable(unittest.TestCase):
    '''Test: Correct truth tables are produced for valid expressions'''
    def setUp(self):
        self.board = Board()
        self.and_gate = And_Gate()
        self.switch1 = Switch()
        self.switch2 = Switch()
        self.output = Output()
        self.board.add_gate(self.and_gate)
        self.board.add_gate(self.switch1)
        self.board.add_gate(self.switch2)
        self.board.add_gate(self.output)
        
    def test_with_valid_expression(self):
        expression = "A AND B"
        tt = generate_truth_table(expression)
        self.assertDictEqual(
            tt[0], 
            {
                'a':[0,0,1,1],
                'b':[0,1,0,1],
                'OUT':[0,0,0,1]
            }
        )
        self.assertEqual(tt[1], expression)
        
    def test_with_invalid_expression(self):
        expression = "AND"
        tt = generate_truth_table(expression)
        self.assertEqual(tt, "Invalid Input")
        
        
        

if __name__ == '__main__':
    unittest.main()