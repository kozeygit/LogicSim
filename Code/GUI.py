## Kivy GUI ##
import sys
import platform
import kivy
kivy.require('2.0.0')

from kivy.app import App
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
from tabulate import tabulate

from logic.board import Board
from logic.gates import *
from logic.truth_table import *

Window.maximize()



class ExitPopup(Popup):
    def close_window(self):
        sys.exit()

class TruthPopup(Popup):
    FONT = StringProperty()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if platform.system() == "Linux":
            self.FONT = "FreeMonoBold"
        else:
            self.FONT = "LUCON"
        
    def open(self, root, *args, **kwargs):
        super().open(*args, **kwargs)
        selectedGate = root.ids["gateCanvas"].get_selected_gates()
        if len(selectedGate) != 1:
            text = 'Enter Boolean Expression Here'
        else:
            text = selectedGate[0].logic_gate.getExpression()
        self.ids["truth_input"].text = text
        self.generate()

    def generate(self):
        input = self.ids["truth_input"].text 
        out = generateTruthTable(input)
        if out == "Invalid Input":
            self.ids["truth_label"].text = ""
        else:
            out2 = tabulate(out[0], headers=out[0].keys(), tablefmt="pretty")
            self.ids["truth_label"].text = f"{out[1]}\n{out2}"
            #print(f"{out[1]}\n{out2}")

class ConnectionLine(Widget):
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
        
    def collide_line(self, x, y):
        print(self.points)
        
    def get_gates(self):
        return (self.out_gate, self.in_gate)
    
    def get_nodes(self):
        return ((self.out_gate, -1), (self.in_gate, self.in_node))

    def get_turn_points(self, out_node_pos, in_node_pos):
        x1 = out_node_pos[0]
        x2 = in_node_pos[0]
        y1 = out_node_pos[1]
        y2 = in_node_pos[1]
        x_mid = (x1 + x2)/2
        turn1 = [x_mid, y1]
        turn2 = [x_mid, y2]
        return turn1 + turn2

    def update_state(self):
        self.state = self.out_gate.get_state()
        self.color_state = self.color_states[self.state]

    def update_pos(self):
        out_node_pos = self.out_gate.get_node_pos(-1)
        in_node_pos = self.in_gate.get_node_pos(self.in_node)
        self.points = out_node_pos + self.get_turn_points(out_node_pos, in_node_pos) + in_node_pos
        self.outline.points = self.points
        self.inline.points = self.points
        #print(self.pos, self.size)


class GateCanvas(FloatLayout):
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
            "clock":None
        }

    def update_connection_lines(self):
        for line in self.connection_lines[:]:
            line.update_pos()

    def update_states(self):
        for gate in self.gates:
            gate.update_state()
        for line in self.connection_lines:
            line.update_state()
    
    def set_tool(self, tool):
        self.tool = tool
        if tool in ("connect", "disconnect"):
            for gate in self.gates[:]:
                gate.show_nodes()
        else:
            for gate in self.gates[:]:
                gate.hode_nodes()
        
    def connect_down(self, touch):
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
                    
                    if self.board.connectGate(in_gate.get_logic_gate(), out_gate.get_logic_gate(), node=in_node):
                        line = ConnectionLine(out_gate, in_gate, in_node)
                        self.connection_lines.append(line)
                        self.add_widget(line)
                    
                    self.update_states()
                        
        for gate in self.gates[:]:
            gate.deselect_nodes()

        self.out_connection = None
        self.in_connection = None
        return True

    def move_down(self, touch):
        for child in self.gates[::-1]:
            if child.dispatch('on_touch_down', touch):
                return True
        if not self.collide_point(*touch.pos):
            return False
        self.deselect_gates()
        return True
    
    def disconnect_down(self, touch):
        self.deselect_gates()
        for gate in self.gates[:]:
            if node := gate.get_node_collide(touch):
                if node == -1:
                    for line in self.connection_lines:
                        gate_node_tuple = line.get_nodes()
                        if gate_node_tuple[0][0] == gate:
                            gate2 = gate_node_tuple[1][0]
                            self.board.disconnectGate(gate2.get_logic_gate(), gate.get_logic_gate())
                            self.connection_lines.remove(line)
                            self.remove_widget(line)
                elif node == 1 or node == 2:
                    for line in self.connection_lines:
                        gate_node_tuple = line.get_nodes()
                        if gate_node_tuple[1] == (gate,node):
                            gate2 = gate_node_tuple[0][0]
                            self.board.disconnectGate(gate.get_logic_gate(), gate2.get_logic_gate())
                            self.connection_lines.remove(line)
                            self.remove_widget(line)
        self.update_states()        
        return True

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos): 
            if touch.is_double_tap and self.tool != "move":
                self.root.set_tool("move")
                return True
            #print(self.board.gates)
            if self.tool == "connect":
                return self.connect_down(touch)
            
            if self.tool == "disconnect":
                return self.disconnect_down(touch)
            
            if self.tool == "move":
                return self.move_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if self.tool == "connect":
                return self.connect_up(touch)
            if self.tool == "disconnect":
                pass
            if self.tool == "move":
                pass
        return super().on_touch_up(touch)
   
    
    def get_selected_gates(self):
        return [child for child in self.gates[:] if child.is_selected()]

    def deselect_gates(self):
        [child.deselect() for child in self.gates[:]]


    def add_gate(self, gate_type):
        new_gate = self.gate_dict[gate_type](parent_rect=(self.x, self.y, self.width, self.height))
        self.add_widget(new_gate)
        self.gates.append(new_gate)
        new_gate.root = self.root
        self.board.addGate(new_gate.get_logic_gate())
        new_gate.update_state()
        #print(self.board.gates)

    def delete_gate(self):
        if not self.tool == "move":
            self.root.set_tool("move")
        else:
            for gate in self.get_selected_gates():
                
                #This is probably a terrible way to do this, so find a better one
                for line in self.connection_lines[:]:
                    if gate in line.get_gates():
                        self.connection_lines.remove(line)
                        self.remove_widget(line)
                
                self.board.removeGate(gate.get_logic_gate())
                self.remove_widget(gate)
                self.gates.remove(gate)
                self.update_states()

    def clear_canvas(self):
        self.board.clearBoard()
        self.clear_widgets()
        self.gates = []
        #print(self.board.gates)


class DragGate(DragBehavior, FloatLayout):
    def __init__(self, parent_rect, **kwargs):
        super().__init__(**kwargs)
        self.drag_rectangle = parent_rect
        self.drag_timeout = 500
        self.drag_distance = 5
        self.allow_stretch = True
        self.size_hint = None, None
        self.size = (100,100)
        self.pos = (parent_rect[0]+parent_rect[2])/2, (parent_rect[1]+parent_rect[3])/2
        
        self.img = Image(pos = self.pos, size_hint = (1,1))
        self.add_widget(self.img)
        
        self.nodes = []
        self.nodes_init()

        self.border = Line(rounded_rectangle = (self.x, self.y, self.width, self.height, 10))
        self.canvas.add(self.border)
        
        self.logic_gate = None
        self.state = None
        self.dragged = False
        self.select()
        #print(self.parent)
    
    def nodes_init(self):
        node_source="Images/GateIcons/node.png"
        self.in_node_1 = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.in_node_2 = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.out_node = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.nodes.append(self.in_node_1)
        self.nodes.append(self.in_node_2)
        self.nodes.append(self.out_node)
        self.add_widget(self.in_node_1)
        self.add_widget(self.in_node_2)
        self.add_widget(self.out_node)
        self.hode_nodes() 

    def get_node_pos(self, node):
        return self.get_node(node).center

    def update_nodes(self):
        self.in_node_1.center=(self.x, self.center_y+26)
        self.in_node_2.center=(self.x, self.center_y-26)
        self.out_node.center=(self.right, self.center_y+2)

    def get_node_collide(self, touch):
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
        node = self.get_node(node_index)
        node.color = (0.3, 0.7, 0.7, 1)

    def deselect_node(self, node_index):
        node = self.get_node(node_index)
        node.color = (1, 1, 1, 1)
    
    def deselect_nodes(self):
        for node in self.nodes:
            node.color = (1, 1, 1, 1)

    def get_node(self, index):
        if index == 1:
            return self.in_node_1
        if index == 2:
            return self.in_node_2
        if index == -1:
            return self.out_node
    
    def on_pos(self, *args, **kwargs):
        try:
            self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 10)
            self.img.pos = self.pos
            self.update_nodes()
            self.parent.update_connections()
        except AttributeError as e:
            print("Gate not finished initalising", e)

    def is_selected(self):
        return self.selected

    def show_nodes(self):
        for i in self.nodes:
            i.opacity = 1
            i.disabled = False
        self.update_nodes()

    def hode_nodes(self):
        for i in self.nodes:
            i.opacity = 0
            i.disabled = True

    def select(self):
        self.selected = True
        self.border.width = 2

    def deselect(self):
        self.selected = False
        self.border.width = 0.0001
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dragged = False
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
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
        return self.logic_gate

    def update_state(self):
        x = self.logic_gate.getOutput()
        #print(self, "I AM UPDATING", x)
        self.state = x

    def get_state(self):
        return self.state

class DragSwitch(DragGate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic_gate = Switch()
        self.states = {1:"Images/GateIcons/switch_on.png", 0:"Images/GateIcons/switch_off.png"}
        self.img.source = self.states[self.logic_gate.getOutput()]

    def nodes_init(self):
        node_source="Images/GateIcons/node.png"
        self.out_node = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.add_widget(self.out_node)
        self.nodes.append(self.out_node)
        self.hode_nodes() 

    def update_nodes(self):
        self.out_node.center=(self.right, self.y+(self.height//2))

    def get_node_collide(self, touch):
        for i in self.nodes:
            if i.collide_point(*touch.pos):
                if i == self.out_node:
                    return -1
        return False

    #for some reason needs a double click to change state
    def on_touch_up(self, touch):
        if self.dragged:
            return super().on_touch_up(touch)
        elif (touch.pos[0] < self.right - 30) and (touch.pos[0] > self.x + 10) and (touch.pos[1] < self.top - 20) and (touch.pos[1] > self.y + 20):
            #print("BUTTTON PRESSED, I REPEAT BUTTON PRESSED", self.dragged)
            self.logic_gate.flip()
            self.update_state()
            self.parent.update_states()
            return True
        return super().on_touch_up(touch)
    
    def update_state(self):
        x = self.logic_gate.getOutput()
        #print(self, "I AM UPDATING", x)
        self.state = x
        self.img.source = self.states[self.state]

class DragOutput(DragGate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic_gate = Output()
        self.states = {1:"Images/GateIcons/output_on.png", 0:"Images/GateIcons/output_off.png", None:"Images/GateIcons/output_empty.png"}
        self.update_state()

    def nodes_init(self):
        node_source="Images/GateIcons/node.png"
        self.in_node_1 = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.add_widget(self.in_node_1)
        self.nodes.append(self.in_node_1)
        self.hode_nodes()

    def update_nodes(self):
        self.in_node_1.center=(self.x, self.center_y)

    def get_node_collide(self, touch):
        for i in self.nodes:
            if i.collide_point(*touch.pos):
                if i == self.in_node_1:
                    return 1
        return False

    def update_state(self):
        x = self.logic_gate.getOutput()
        #print(self, "I AM UPDATING", x)
        self.state = x
        self.img.source = self.states[self.state]


class DragAndGate(DragGate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img.source = "Images/GateIcons/and.png"
        self.logic_gate = And_Gate()

class DragOrGate(DragGate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img.source = "Images/GateIcons/or.png"
        self.logic_gate = Or_Gate()

class DragXorGate(DragGate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img.source = "Images/GateIcons/xor.png"
        self.logic_gate = Xor_Gate()

class DragNotGate(DragGate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img.source = "Images/GateIcons/not.png"
        self.logic_gate = Not_Gate()

    def nodes_init(self):
        node_source="Images/GateIcons/node.png"
        self.in_node_1 = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.out_node = Image(source=node_source, size_hint=(None, None), size=(20,20))
        self.add_widget(self.in_node_1)
        self.add_widget(self.out_node)
        self.nodes.append(self.in_node_1)
        self.nodes.append(self.out_node)
        self.hode_nodes()

    def update_nodes(self):
        self.in_node_1.center=(self.x, self.center_y+2)
        self.out_node.center=(self.right, self.center_y+2)

    def get_node_collide(self, touch):
        for node in self.nodes:
            if node.collide_point(*touch.pos):
                if node == self.in_node_1:
                    return 1
                elif node == self.out_node:
                    return -1
        return False


class MainWindow(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids["gateCanvas"].root = self
        self.toggles = ["connectToggle", "moveToggle", "disconnectToggle"]
        
    def set_tool(self, tool):
        self.ids["gateCanvas"].set_tool(tool)
        self.ids["toolLabel"].text = tool
        toggle = f"{tool}Toggle"
        if self.ids[toggle].state == 'down':
            pass
        else:
            for i in self.toggles:
                if i == toggle:
                    self.ids[i].state = 'down'
                else:
                    self.ids[i].state = 'normal'
    
    def clear_canvas(self):
        self.ids["gateCanvas"].clear_canvas()

    def delete_gate(self):
        self.ids["gateCanvas"].delete_gate()
        self.set_tool("move")

    def add_gate(self, gate_type):
        self.ids["gateCanvas"].add_gate(gate_type)
        
kv = Builder.load_file("test.kv")

class LogicGateSimulator(App):
    def build(self):
        #self.icon = "Images/Me.jpg"
        return MainWindow()

if __name__ == '__main__':
    LogicGateSimulator().run()
