## Kivy GUI ##
import kivy, os, sys
import logging
kivy.require('2.0.0')
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle, Ellipse
from kivy.graphics.svg import Svg
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from logic.board import Board
from logic.gates import *
from logic.truth_table import *

Window.maximize()

class ExitPopup(Popup):
    def closeWindow(self):
        sys.exit()

class TruthPopup(Popup):
    def generate(self):
        input = self.ids["truth_input"].text 
        out = generateTruthTable(input)
        
        self.ids["truth_label"].text = input
        print("TRUTH TABLE GENERATED\n"*5)

class ConnectionLine(Widget):
    def __init__(self, outGate, inGate, inNode):
        self.out_gate = outGate
        self.in_gate = inGate
        self.in_gate_node = inNode
        self.state = None
        self.line = Line()
    pass


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
            "input":DragSwitch,
            "output":DragOutput,
            "clock":None
        }

    def updateStates(self):
        print("updating")
        for i in self.gates:
            i.update_state()
    
    # i have no idea how to do this??
    def addConnectionLine(self, exit_gate, input_gate, input_node):
        line = ConnectionLine()
    
    def setTool(self, tool):
        self.tool = tool
        if tool in ("connect", "disconnect"):
            for i in self.gates[:]:
                i.showNodes()
        else:
            for i in self.gates[:]:
                i.hideNodes()

        
    def connect_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        self.deselectGates()
        for child in self.gates[:]:
            if node := child.getNodeCollide(touch):
                if node == -1:
                    self.out_connection = (node, child)
                else:
                    self.in_connection = (node, child)
                child.selectNode(node)
                return True
        return True


    def connect_up(self, touch):
        for child in self.gates[:]:
            if node := child.getNodeCollide(touch):
                if node == -1:
                    self.out_connection = (node, child)
                else:
                    self.in_connection = (node, child)
                child.selectNode(node)
                
                in_gate = self.in_connection[1]
                out_gate = self.out_connection[1]
                in_node = self.in_connection[0]
                self.board.connectGate(in_gate.getLogicGate(), out_gate.getLogicGate(), node=in_node)
                (i.update_state() for i in self.gates[:])
                self.connection_lines.append(Line(points=(in_gate.pos, out_gate.pos)))
                self.canvas.add(self.connection_lines[-1])
                self.updateStates()
            else:
                self.deselectGates()
        return True

    def move_down(self, touch):
        for child in self.gates[:]:
            if child.dispatch('on_touch_down', touch):
                return True
        if not self.collide_point(*touch.pos):
            return False
        self.deselectGates()
        return True

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos): 
            if touch.is_double_tap and self.tool != "move":
                self.root.setTool("move")
                return True
            #print(self.board.gates)
            if self.tool == "connect":
                return self.connect_down(touch)
            if self.tool == "disconect":
                pass
            if self.tool == "move":
                return self.move_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if self.tool == "connect":
                return self.connect_up(touch)
            if self.tool == "disconect":
                pass
            if self.tool == "move":
                return super().on_touch_up(touch)
        return super().on_touch_up(touch)
   
    
    def getSelectedGates(self):
        return [child for child in self.gates[:] if child.isSelected()]

    def deselectGates(self):
        [child.deselect() for child in self.gates[:]]


    def addGate(self, gate_type):
        new_gate = self.gate_dict[gate_type](parent_rect=(self.x, self.y, self.width, self.height))
        self.add_widget(new_gate)
        self.gates.append(new_gate)
        new_gate.root = self.root
        self.board.addGate(new_gate.getLogicGate())
        new_gate.update_state()
        #print(self.board.gates)

    def deleteGates(self):
        if not self.tool == "move":
            self.root.setTool("move")
        else:
            for i in self.getSelectedGates():
                self.board.removeGate(i.getLogicGate())
                self.remove_widget(i)
                self.gates.remove(i)
                self.updateStates()

    def clearCanvas(self):
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
        self.in_node_1 = Image(source=node_source, pos=(self.x-6, self.top-29), size_hint=(None, None), size=(12,12))
        self.in_node_2 = Image(source=node_source, pos=(self.x-6, self.y+18), size_hint=(None, None), size=(12,12))
        self.out_node = Image(source=node_source, pos=(self.right-6, self.y+(self.height//2)-4), size_hint=(None, None), size=(12,12))
        self.nodes.append(self.in_node_1)
        self.nodes.append(self.in_node_2)
        self.nodes.append(self.out_node)
        self.add_widget(self.in_node_1)
        self.add_widget(self.in_node_2)
        self.add_widget(self.out_node)
        self.hideNodes() 

    def nodes_update(self):
        self.in_node_1.pos=(self.x-6, self.top-29)
        self.in_node_2.pos=(self.x-6, self.y+18)
        self.out_node.pos=(self.right-6, self.y+(self.height//2)-4)

    def getNodeCollide(self, touch):
        for i in self.nodes:
            if i.collide_point(*touch.pos):
                if i == self.in_node_1:
                    return 0
                elif i == self.in_node_2:
                    return 1
                elif i == self.out_node:
                    return -1
        return False

    def selectNode(self, node_index):
        node = self.getNode(node_index)
        node.color = (0.3, 0.7, 0.7, 1)

    def deselectNode(self, node_index):
        node = self.getNode(node_index)
        node.color = (1, 1, 1, 1)
    
    def getNode(self, index):
        if index == 0:
            return self.input_node_1
        if index == 1:
            return self.input_node_2
        if index == -1:
            return self.out_node
    
    def on_pos(self, *args, **kwargs):
        try:
            self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 10)
            self.img.pos = self.pos
            self.nodes_update()
        #self.nodes
        except AttributeError as e:
            print("Gate not made yet", e)

    def isSelected(self):
        return self.selected

    def showNodes(self):
        for i in self.nodes:
            i.opacity = 1
            i.disabled = False

    def hideNodes(self):
        for i in self.nodes:
            i.opacity = 1
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

    def getLogicGate(self):
        return self.logic_gate

    def update_state(self):
        x = self.logic_gate.getOutput()
        print(self, "I AM UPDATING", x)
        self.state = x

class DragSwitch(DragGate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic_gate = Switch()
        self.states = {1:"Images/GateIcons/switch_on.png", 0:"Images/GateIcons/switch_off.png"}
        self.img.source = self.states[self.logic_gate.getOutput()]

    def nodes_init(self):
        node_source="Images/GateIcons/node.png"
        self.out_node = Image(source=node_source, pos=(self.right-6, self.y+(self.height//2)-4), size_hint=(None, None), size=(12,12))
        self.add_widget(self.out_node)
        self.nodes.append(self.out_node)
        self.hideNodes() 

    def nodes_update(self):
        self.out_node.pos=(self.right-6, self.y+(self.height//2)-4)

    #accounts for if user wants to change state
    def on_touch_up(self, touch):
        if self.dragged:
            return super().on_touch_up(touch)
        elif (touch.pos[0] < self.right - 30) and (touch.pos[0] > self.x + 10) and (touch.pos[1] < self.top - 20) and (touch.pos[1] > self.y + 20):
            print("BUTTTON PRESSED, I REPEAT BUTTON PRESSED", self.dragged)
            self.logic_gate.flip()
            self.update_state()
            self.parent.updateStates()
            return True
        return super().on_touch_up(touch)
    
    def update_state(self):
        x = self.logic_gate.getOutput()
        print(self, "I AM UPDATING", x)
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
        self.in_node_1 = Image(source=node_source, pos=(self.x-6, self.y+(self.height//2)-4), size_hint=(None, None), size=(12,12))
        self.add_widget(self.in_node_1)
        self.nodes.append(self.in_node_1)
        self.hideNodes()

    def nodes_update(self):
        self.in_node_1.pos=(self.x-6, self.y+(self.height//2)-4)

    def update_state(self):
        x = self.logic_gate.getOutput()
        print(self, "I AM UPDATING", x)
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
        self.in_node_1 = Image(source=node_source, pos=(self.x-6, self.y+(self.height//2)-4), size_hint=(None, None), size=(12,12))
        self.out_node = Image(source=node_source, pos=(self.right-6, self.y+(self.height//2)-4), size_hint=(None, None), size=(12,12))
        self.add_widget(self.in_node_1)
        self.add_widget(self.out_node)
        self.nodes.append(self.in_node_1)
        self.nodes.append(self.out_node)
        self.hideNodes()

    def nodes_update(self):
        self.in_node_1.pos=(self.x-6, self.y+(self.height//2)-4)
        self.out_node.pos=(self.right-6, self.y+(self.height//2)-4)


class MainWindow(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids["gateCanvas"].root = self
        self.toggles = ["connectToggle", "moveToggle", "disconnectToggle"]

    def setTool(self, tool):
        self.ids["gateCanvas"].setTool(tool)
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
    
    def clearCanvas(self):
        self.ids["gateCanvas"].clearCanvas()

    def deleteGates(self):
        self.ids["gateCanvas"].deleteGates()
        self.setTool("move")

    def addGateToCanvas(self, gate_type):
        self.ids["gateCanvas"].addGate(gate_type)
        
kv = Builder.load_file("test.kv")

class LogicGateSimulator(App):
    def build(self):
        #self.icon = "Images/Me.jpg"
        return MainWindow()

if __name__ == '__main__':
    LogicGateSimulator().run()
