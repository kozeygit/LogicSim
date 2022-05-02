'''Doctrings Incomplete'''

## Kivy GUI ##
from ast import Str
import sys
import platform
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.utils import rgba
from tabulate import tabulate

from logic.board import Board
from logic.gates import *
from logic.truth_table import *


Window.maximize()


class ExitPopup(Popup):
    '''Popup that opens when quit button is pressed.'''
    def close_window(self):
        '''Exits program.'''
        sys.exit()


class TruthPopup(Popup):
    '''Popup for truth table generator.'''
    FONT = StringProperty()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if platform == 'linux':
            self.FONT = "FreeMonoBold"
        else:
            self.FONT = "LUCON"
        
    def open(self, root, *args, **kwargs):
        '''Overwrite of kivy method, inserts selected components expression into input field.'''
        super().open(*args, **kwargs)
        selected_gate = root.ids["gateCanvas"].get_selected_gates()
        if len(selected_gate) != 1:
            text = 'Enter Boolean Expression Here'
        else:
            text = selected_gate[0].logic_gate.get_expression()
        self.ids["truth_input"].text = text
        self.generate()

    def generate(self):
        '''Using expression in input field, generates a truth table and diplays it.'''
        input_expression = self.ids["truth_input"].text 
        out = generate_truth_table(input_expression)
        if out == "Invalid Input":
            if input_expression == "Enter Boolean Expression Here":
                self.ids["truth_label"].text = "Truth table will appear here"
            else:
                self.ids["truth_label"].text = "Invalid Input."
        else:
            out2 = tabulate(out[0], headers=out[0].keys(), tablefmt="pretty")
            self.ids["truth_label"].text = f"{out[1]}\n{out2}"


class ConnectionLine(Widget):
    '''Class for lines that connects components together'''
    color_state = ListProperty()
    def __init__(self, out_gate, in_gate, in_node, **kwargs):
        super().__init__(**kwargs)
        self.color_states = {None:(1,1,1,1), 0:(1,0,0,1), 1:(0,1,0,1)}
        self.color_state = (1,1,1,1)
        self.out_gate = out_gate
        self.in_gate = in_gate
        self.in_node = in_node
        self.points = []
        self.state = None
        self.inline = Line(points=self.points, width=1.5, cap='round', joint='round')
        self.outline = Line(points=self.points, width=4, cap='round', joint='round')
        self.canvas.add(self.inline)
        self.canvas.before.add(Color(rgba=(0,0,0,1)))
        self.canvas.before.add(self.outline)
        self.update_pos()
        self.update_state()
        
    def get_gates(self):
        '''Returns tuple: (component line is exiting, component line is entering)'''
        return (self.out_gate, self.in_gate)
    
    def get_nodes(self):
        '''Returns tuple: (component line is exiting, node its exiting), (component line is entering, node its entering))'''
        return ((self.out_gate, -1), (self.in_gate, self.in_node))

    def get_turn_points(self, out_node_pos, in_node_pos):
        '''Returns the extra points to make the line the shape it is <<<<<'''
        x1 = out_node_pos[0]
        x2 = in_node_pos[0]
        y1 = out_node_pos[1]
        y2 = in_node_pos[1]
        x_mid = (x1 + x2)/2
        turn1 = [x_mid, y1]
        turn2 = [x_mid, y2]
        return turn1 + turn2

    def update_state(self):
        '''Updates colour of line to match the output of the component its exiting.'''
        self.state = self.out_gate.get_state()
        self.color_state = self.color_states[self.state]

    def update_pos(self):
        '''Updates the points of the line to match the position of the components its connect to.'''
        out_node_pos = self.out_gate.get_node_pos(-1)
        in_node_pos = self.in_gate.get_node_pos(self.in_node)
        self.points = out_node_pos + self.get_turn_points(out_node_pos, in_node_pos) + in_node_pos
        self.outline.points = self.points
        self.inline.points = self.points


class GateCanvas(FloatLayout):
    '''Canvas where components and connection lines are placed onto'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connection_lines = []
        self.in_connection = None
        self.out_connection = None
        self.gates = []
        
        self.tool = "move"
        self.board = Board()
        self.gate_dict = {
            "and":DragAndGate,
            "or":DragOrGate,
            "not":DragNotGate,
            "xor":DragXorGate,
            "switch":DragSwitch,
            "output":DragOutput,
            "clock":DragClock
        }
        
    def add_connection_line(self, out_gate, in_gate, in_node):
        '''Creates connection line.'''
        line = ConnectionLine(out_gate, in_gate, in_node)
        self.connection_lines.append(line)
        self.add_widget(line)

    def update_connection_lines(self):
        '''Updates the postions of all connection lines on the canvas'''
        for line in self.connection_lines[:]:
            line.update_pos()

    def update_states(self):
        '''Updates the states of all components and connection lines on the canvas'''
        for gate in self.gates:
            gate.update_state()
        for line in self.connection_lines:
            line.update_state()
    
    def set_tool(self, tool):
        '''Sets the tool, can be move, connect, disconnect'''
        self.tool = tool
        if tool is "move":
            for gate in self.gates[:]:
                gate.hide_nodes()
        else:
            for gate in self.gates[:]:
                gate.show_nodes()
                self.deselect_gates()
        
    def on_touch_down(self, touch):
        '''Checks if there is a touch down within the canvas. If touch is double click, set tool to move. Calls a method based on the current tool if single click.'''
        if self.collide_point(*touch.pos): 
            if touch.is_double_tap and self.tool != "move":
                self.root.set_tool("move")
                return True
            if self.tool == "connect":
                return self.connect_down(touch)
            
            if self.tool == "disconnect":
                return self.disconnect_down(touch)
            
            if self.tool == "move":
                return self.move_down(touch)

    def on_touch_up(self, touch):
        '''Checks if there is a touch up within the canvas, Calls a method based on the cuurent tool if there is'''
        if self.collide_point(*touch.pos):
            if self.tool == "connect":
                return self.connect_up(touch)
            if self.tool == "disconnect":
                pass
            if self.tool == "move":
                pass
        return super().on_touch_up(touch)
        
    def connect_down(self, touch):
        '''Checks for node collision on touch down. If collision replace either out_connection or in_connection attribute with (node, gate) tuple'''
        self.deselect_gates()
        for gate in self.gates[:]:
            if node := gate.get_node_collide(touch):
                if node == -1:
                    self.out_connection = (node, gate)
                else:
                    self.in_connection = (node, gate)
                gate.select_node(node)
                return True
        return True

    def connect_up(self, touch):
        '''Checks for node collision on touch up. If collision, replace either out_connection or in_connection attribute with (node, gate) tuple.
        If out_connection and in_connection both have values, connects the component nodes together'''
        for gate in self.gates[:]:
            if node := gate.get_node_collide(touch):
                if node == -1:
                    self.out_connection = (node, gate)
                else:
                    self.in_connection = (node, gate)
                gate.select_node(node)
                
                if self.in_connection is None:
                    print("Can't connect output to output")
                elif self.out_connection is None:
                    print("Cant connect input to input")
                else:
                    in_gate = self.in_connection[1]
                    out_gate = self.out_connection[1]
                    in_node = self.in_connection[0]
                    
                    if self.board.connect_gate(in_gate.get_logic_gate(), out_gate.get_logic_gate(), node=in_node):
                        self.add_connection_line(out_gate, in_gate, in_node)
            
                    self.update_states()
                        
        for gate in self.gates[:]:
            gate.deselect_nodes()

        self.out_connection = None
        self.in_connection = None
        return True

    def move_down(self, touch):
        '''Calls on_touch_down method for children. If canvas clicked instead of a child, deselects all gates.'''
        for child in self.gates[::-1]:
            if child.dispatch('on_touch_down', touch):
                return True
        if not self.collide_point(*touch.pos):
            return False
        self.deselect_gates()
        return True
    
    def disconnect_down(self, touch):
        '''Checks for node collision on touch down. If collision, disconnect clicked node from any nodes its connected to and remove connection lines.'''
        self.deselect_gates()
        for gate in self.gates[:]:
            if node := gate.get_node_collide(touch):
                
                if node == -1:
                    for line in self.connection_lines:
                        gate_node_tuple = line.get_nodes()
                        if gate_node_tuple[0][0] == gate:
                            gate2 = gate_node_tuple[1][0]
                            self.board.disconnect_gate(gate2.get_logic_gate(), gate.get_logic_gate())
                            self.connection_lines.remove(line)
                            self.remove_widget(line)
                
                elif node == 1 or node == 2:
                    for line in self.connection_lines:
                        gate_node_tuple = line.get_nodes()
                        if gate_node_tuple[1] == (gate,node):
                            gate2 = gate_node_tuple[0][0]
                            self.board.disconnect_gate(gate.get_logic_gate(), gate2.get_logic_gate())
                            self.connection_lines.remove(line)
                            self.remove_widget(line)
        self.update_states()        
        return True
    
    def get_selected_gates(self):
        '''Returns a list of all components that are selected.'''
        return [child for child in self.gates[:] if child.is_selected()]

    def deselect_gates(self):
        '''Deselects all selected components.'''
        [child.deselect() for child in self.gates[:]]

    def add_gate(self, gate_type):
        '''Creates new visual component and adds it to canvas, adds logic component to logic board.'''
        new_gate = self.gate_dict[gate_type](parent_rect=(self.x, self.y, self.width, self.height))
        self.add_widget(new_gate)
        self.gates.append(new_gate)
        new_gate.root = self.root
        self.board.add_gate(new_gate.get_logic_gate())
        new_gate.update_state()

    def delete_gate(self):
        '''Deletes selected components from canvas and logic board, also removes any connection lines they are connected to.'''
        if not self.tool == "move":
            self.root.set_tool("move")
        else:
            for gate in self.get_selected_gates():
                
                #This is probably a terrible way to do this, so find a better one
                for line in self.connection_lines[:]:
                    if gate in line.get_gates():
                        self.connection_lines.remove(line)
                        self.remove_widget(line)
                        del line
                
                self.board.remove_gate(gate.get_logic_gate())
                self.remove_widget(gate)
                self.gates.remove(gate)
                del gate
                self.update_states()

    def clear_canvas(self):
        '''Deletes all components from canvas and logic board'''
        self.board.clear_board()
        self.clear_widgets()
        self.gates = []


class DragGate(DragBehavior, FloatLayout):
    '''Visual components parent class. DOCSRINGS NOT DONE'''
    def __init__(self, parent_rect, **kwargs):
        super().__init__(**kwargs)
        '''Sets kivy properties'''
        self.drag_rectangle = parent_rect
        self.drag_timeout = 500
        self.drag_distance = 5
        self.allow_stretch = True
        self.size_hint = None, None
        self.size = (100,100)
        self.pos = (parent_rect[0]+parent_rect[2])/2, (parent_rect[1]+parent_rect[3])/2
        '''Sets image of component'''
        self.img = Image(pos = self.pos, size_hint = (1,1))
        self.add_widget(self.img)
        '''Initialises the nodes of the component and adds them to node array'''
        self.nodes = []
        self.nodes_init()
        '''Creates the selection border and adds to component.'''
        self.border = Line(rounded_rectangle = (self.x, self.y, self.width, self.height, 10))
        self.canvas.add(Color(0,0,0,1))
        self.canvas.add(self.border)
        '''Creates a parallel logic version of the component. None in parent class.'''
        self.logic_gate = None
        self.state = None
        '''Creates dragged attribute and selects the component.'''
        self.dragged = False
        self.select()
        
    def nodes_init(self):
        '''Initialises the nodes of the component, positions them and adds them to the component widget.'''
        node_source="GateIcons/node.png"
        self.in_node_1 = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.in_node_2 = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.out_node = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.nodes.append(self.in_node_1)
        self.nodes.append(self.in_node_2)
        self.nodes.append(self.out_node)
        self.add_widget(self.in_node_1)
        self.add_widget(self.in_node_2)
        self.add_widget(self.out_node)
        self.hide_nodes() 

    def get_node_pos(self, node):
        '''Return the coordinates of the given node.'''
        return self.get_node(node).center

    def update_nodes(self):
        '''Updates the positions of the components nodes.'''
        self.in_node_1.center=(self.x, self.center_y+26)
        self.in_node_2.center=(self.x, self.center_y-26)
        self.out_node.center=(self.right, self.center_y+2)

    def get_node_collide(self, touch):
        '''Returns node index if the user has clicked a node.'''
        for node in self.nodes:
            if node.collide_point(*touch.pos):
                if node == self.in_node_1:
                    return 1
                elif node == self.in_node_2:
                    return 2
                elif node == self.out_node:
                    return -1
        return False

    def select_node(self, node_index):
        '''Selects the given node.'''
        node = self.get_node(node_index)
        node.color = (0.3, 0.7, 0.7, 1)

    def deselect_node(self, node_index):
        '''Deselects the given node.'''
        node = self.get_node(node_index)
        node.color = (1, 1, 1, 1)
    
    def deselect_nodes(self):
        '''Deselects all node of component.'''
        for node in self.nodes:
            node.color = (1, 1, 1, 1)

    def get_node(self, index):
        '''Returns the node object for given node index.'''
        if index == 1:
            return self.in_node_1
        if index == 2:
            return self.in_node_2
        if index == -1:
            return self.out_node
    
    def on_pos(self, *args, **kwargs):
        '''Listens for change of kivy pos property. Updates position of image, nodes and selection border. Also tells board to update position of connection lines.'''
        try:
            self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 10)
            self.img.pos = self.pos
            self.update_nodes()
            self.parent.update_connection_lines()
        except AttributeError as e:
            print("Gate not finished initalising", e)

    def is_selected(self):
        '''Returns True if component is currently selected.'''
        return self.selected

    def show_nodes(self):
        '''Shows the components nodes.'''
        for node in self.nodes:
            node.opacity = 1
            node.disabled = False
        self.update_nodes()

    def hide_nodes(self):
        '''Hides the components nodes.'''
        for node in self.nodes:
            node.opacity = 0
            node.disabled = True

    def select(self):
        '''Selects the component.'''
        self.selected = True
        self.border.width = 2

    def deselect(self):
        '''Deselects the component'''
        self.selected = False
        self.border.width = 0.0001
    
    def on_touch_down(self, touch):
        '''Checks if user has clicked node, sets dragged attribute to false.'''
        if self.collide_point(*touch.pos):
            self.dragged = False
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        '''Checks if the user drags the component when clicked. Sets dragged attribute to true, selectes component updates position if user drags within the drag_timeout time and a distance greater than the drag_distance distance.'''
        if touch.grab_current is not self:
            return super().on_touch_move(touch)
        self.select()
        self.dragged = True
        if self.x < self.parent.x+5:
            self.x = self.parent.x+5
        elif self.y < self.parent.y+5:
            self.y = self.parent.y+5
        elif self.right > self.parent.right-5:
            self.right = self.parent.right-5
        elif self.top > self.parent.top-5:
            self.top = self.parent.top-5
        else:
            return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        '''When user releases click, checks dragged attribute, if true component is deselected, if false and the component is already selected the component is also deselected, if both false component is selected.'''
        if not self.collide_point(*touch.pos):
            return super().on_touch_up(touch)
        if self.dragged:
            self.deselect()
        elif self.selected:
            self.deselect()
        else:
            self.select()
        return super().on_touch_up(touch)

    def get_logic_gate(self):
        '''Returns the logic component object of this visual component object.'''
        return self.logic_gate

    def update_state(self):
        '''Updates the state of component to match state of logic component.'''
        x = self.logic_gate.get_output()
        self.state = x

    def get_state(self):
        '''Returns the components state.'''
        return self.state

class DragSwitch(DragGate):
    '''Switch visual component. User sets state of component'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic_gate = Switch()
        self.states = {1:"GateIcons/switch_on.png", 0:"GateIcons/switch_off.png"}
        self.img.source = self.states[self.logic_gate.get_output()]

    def nodes_init(self):
        '''Initialises the nodes of the component, positions them and adds them to the component widget.'''
        node_source="GateIcons/node.png"
        self.out_node = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.add_widget(self.out_node)
        self.nodes.append(self.out_node)
        self.hide_nodes() 

    def update_nodes(self):
        '''Updates the positions of the components nodes.'''
        self.out_node.center=(self.right, self.y+(self.height//2))

    def get_node_collide(self, touch):
        '''Returns node index if the user has clicked a node.'''
        for node in self.nodes:
            if node.collide_point(*touch.pos):
                if node == self.out_node:
                    return -1
        return False

    def on_touch_up(self, touch):
        '''When user releases click, checks dragged attribute, if false and the touch is within the set area, the switch is flipped and dragged is set as true, then super of method is called.'''
        if not self.dragged:
            if (touch.pos[0] < self.right - 30) and (touch.pos[0] > self.x + 10) and (touch.pos[1] < self.top - 20) and (touch.pos[1] > self.y + 20):
                self.logic_gate.flip()
                self.update_state()
                self.parent.update_states()
                self.dragged = True
        return super().on_touch_up(touch)
    
    def update_state(self):
        '''Updates the state of component to match state of logic component.'''
        x = self.logic_gate.get_output()
        self.state = x
        self.img.source = self.states[self.state]

class DragClock(DragGate):
    '''Clock visual component. Kivy scheduler flips state after an interval. (Uses switch logic component.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic_gate = Switch()
        
        self.states = {1:"GateIcons/clock_on.png", 0:"GateIcons/clock_off.png"}
        self.img.source = self.states[self.logic_gate.get_output()]
        Clock.schedule_interval(self.clock_flip, 1)

    def clock_flip(self, *args):
        '''Flips state of logic component, if AttributeError, the clock has been deleted so it stop the kivy schedule.'''
        self.logic_gate.flip()
        self.update_state()
        try:
            self.parent.update_states()
        except AttributeError as e:
            print("Clock must have been deleted")
            Clock.unschedule(self.clock_flip)

    def nodes_init(self):
        '''Initialises the nodes of the component, positions them and adds them to the component widget.'''
        node_source="GateIcons/node.png"
        self.out_node = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.add_widget(self.out_node)
        self.nodes.append(self.out_node)
        self.hide_nodes()

    def update_nodes(self):
        '''Updates the positions of the components nodes.'''
        self.out_node.center=(self.right, self.y+(self.height//2))

    def get_node_collide(self, touch):
        '''Returns node index if the user has clicked a node.'''
        for node in self.nodes:
            if node.collide_point(*touch.pos):
                if node == self.out_node:
                    return -1
        return False
    
    def update_state(self):
        '''Updates the state of component to match state of logic component.'''
        x = self.logic_gate.get_output()
        self.state = x
        self.img.source = self.states[self.state]

class DragOutput(DragGate):
    '''Output visual component. Displays its state.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic_gate = Output()
        self.states = {1:"GateIcons/output_on.png", 0:"GateIcons/output_off.png", None:"GateIcons/output_empty.png"}
        self.update_state()

    def nodes_init(self):
        '''Initialises the nodes of the component, positions them and adds them to the component widget.'''
        node_source="GateIcons/node.png"
        self.in_node_1 = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.add_widget(self.in_node_1)
        self.nodes.append(self.in_node_1)
        self.hide_nodes()

    def update_nodes(self):
        '''Updates the positions of the components nodes.'''
        self.in_node_1.center=(self.x, self.center_y)

    def get_node_collide(self, touch):
        '''Returns node index if the user has clicked a node.'''
        for node in self.nodes:
            if node.collide_point(*touch.pos):
                if node == self.in_node_1:
                    return 1
        return False

    def update_state(self):
        '''Updates the state of component to match state of logic component.'''
        x = self.logic_gate.get_output()
        self.state = x
        self.img.source = self.states[self.state]


class DragAndGate(DragGate):
    '''And Gate visual component.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img.source = "GateIcons/and.png"
        self.logic_gate = And_Gate()

class DragOrGate(DragGate):
    '''And Or visual component.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img.source = "GateIcons/or.png"
        self.logic_gate = Or_Gate()

class DragXorGate(DragGate):
    '''And Xor visual component.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img.source = "GateIcons/xor.png"
        self.logic_gate = Xor_Gate()

class DragNotGate(DragGate):
    '''Not Gate visual component.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img.source = "GateIcons/not.png"
        self.logic_gate = Not_Gate()

    def nodes_init(self):
        '''Initialises the nodes of the component, positions them and adds them to the component widget.'''
        node_source="GateIcons/node.png"
        self.in_node_1 = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.out_node = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.add_widget(self.in_node_1)
        self.add_widget(self.out_node)
        self.nodes.append(self.in_node_1)
        self.nodes.append(self.out_node)
        self.hide_nodes()

    def update_nodes(self):
        '''Updates the positions of the components nodes.'''
        self.in_node_1.center=(self.x, self.center_y+2)
        self.out_node.center=(self.right, self.center_y+2)

    def get_node_collide(self, touch):
        '''Returns node index if the user has clicked a node.'''
        for node in self.nodes:
            if node.collide_point(*touch.pos):
                if node == self.in_node_1:
                    return 1
                elif node == self.out_node:
                    return -1
        return False


class MainWindow(Widget):
    '''Main Window class'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids["gateCanvas"].root = self
        self.toggles = ["connectToggle", "moveToggle", "disconnectToggle"]
        
    def set_tool(self, tool):
        '''Calls Gate Canvases set_tool method.'''
        self.ids["gateCanvas"].set_tool(tool)
        toggle = f"{tool}Toggle"
        if self.ids[toggle].state == 'down':
            pass
        else:
            for tog in self.toggles:
                if tog == toggle:
                    self.ids[tog].state = 'down'
                else:
                    self.ids[tog].state = 'normal'
    
    def clear_canvas(self):
        '''Calls Gate Canvases clear_canvas method.'''
        self.ids["gateCanvas"].clear_canvas()
        self.set_tool("move")

    def add_gate(self, gate_type):
        '''Calls Gate Canvases add_gate method.'''
        self.ids["gateCanvas"].add_gate(gate_type)
        
    def delete_gate(self):
        '''Calls Gate Canvases delete_gate method.'''
        self.ids["gateCanvas"].delete_gate()
        self.set_tool("move")


kv = Builder.load_file("LogicSim.kv")
'''Loads the kivy file'''

class LogicGateSimulator(App):
    '''Kivy App class.'''
    
    colours = [
        '222222',
        '062037',
        '748bb4',
        'DCDCDC',
        'f1c4a5',
        'FFFFFF',
        '000000'
        ]
    DARK_GREY = StringProperty(colours[0])
    col2 = StringProperty(colours[1])
    BLUE = StringProperty(colours[2])
    LIGHT_GREY = StringProperty(colours[3])
    ORANGE = StringProperty(colours[4])
    WHITE = StringProperty(colours[5])
    BLACK = StringProperty(colours[6])
    
    def build(self):
        '''Builds the kivy app.'''
        self.icon = "GateIcons/and.png"
        return MainWindow()

if __name__ == '__main__':
    LogicGateSimulator().run()
