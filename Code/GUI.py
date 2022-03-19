## Kivy GUI ##
import kivy, os, sys
import logging
kivy.require('2.0.0')
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
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

Window.maximize()

class ExitPopup(Popup):
    def closeWindow(self):
        sys.exit()

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

    # i have no idea how to do this??
    def addConnectionLine(self, exit_gate, input_gate, input_node):
        line = ConnectionLine()
    
    def setTool(self, tool):
        self.tool = tool
    
    def connect(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        self.deselectGates()
        for child in self.gates[:]:
            if child.collide_point(*touch.pos):
                child.select()
                return True
        return True

    

    def move(self, touch):
        #if the touch is not for me, and if i don't want to use it, avoid it.
        for child in self.gates[:]:
            if child.dispatch('on_touch_down', touch):
                return True
        if not self.collide_point(*touch.pos):
            return False
        self.deselectGates()
        return True

    def on_touch_down(self, touch):
        #print(self.board.gates)
        if self.tool == "connect":
            return self.connect(touch)
        if self.tool == "disconect":
            pass
        if self.tool == "move":
            return self.move(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if self.tool == "connect":
                for child in self.gates[:]:
                    if child.collide_point(*touch.pos):
                        if child not in self.getSelectedGates():
                            child.select()
                            print(len(self.getSelectedGates()))
                            node = self.board.connectGate(self.getSelectedGates()[1].getLogicGate(), self.getSelectedGates()[0].getLogicGate())
                            (i.update_state() for i in self.gates[:])
                            return True
                        else:
                            self.deselectGates()
            if self.tool == "disconect":
                pass
            if self.tool == "move":
                return super().on_touch_up(touch)
            print(self.getSelectedGates())
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
        #print(self.board.gates)

    def deleteGates(self):
        if not self.tool == "move":
            self.tool = "move"
        else:
            for i in self.getSelectedGates():
                self.board.removeGate(i.getLogicGate())
                self.remove_widget(i)
                self.gates.remove(i)

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
        self.border = Line(rounded_rectangle = (self.x, self.y, self.width, self.height, 10))
        self.canvas.add(self.border)
        
        self.root = None
        self.nodes = []
        self.logic_gate = None
        self.dragged = False
        self.select()
        #print(self.parent)

    def isSelected(self):
        return self.selected

    def showNodes(self):
        for node in self.nodes:
            self.nodes.colour

    def hideNodes(self):
        for node in self.nodes:
            self.remove_widget(node)

    def select(self):
        self.selected = True
        self.border.width = 2
        #print(self.root)

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
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 10)
        self.img.pos = self.pos
        
        if self.x < self.parent.x:
            self.x = self.parent.x
        elif self.y < self.parent.y:
            self.y = self.parent.y
        elif self.right > self.parent.right:
            self.right = self.parent.right
        elif self.top > self.parent.top:
            self.top = self.parent.top
        else:
            #print(self.pos)
            pass
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
        pass

class DragSwitch(DragGate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic_gate = Switch()
        self.toggle = Rectangle(pos=self.pos, size=self.size)
        self.canvas.add(self.toggle)
        self.bind(pos=self.redraw, size=self.redraw)

        
        self.toggle = Rectangle(pos=(self.pos), size=(self.size))
        self.states = {1:"Images/GateIcons/switch_on.png", 0:"Images/GateIcons/switch_off.png"}
        self.img.source = self.states[self.logic_gate.getOutput()]

    def redraw(self, *args):
        self.toggle.size = self.size
        self.toggle.pos = self.pos

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dragged = False
            #print(self.logic_gate.getOutput())
        return super().on_touch_down(touch)

    def update_state(self):
        self.img.source = self.states[self.logic_gate.getOutput()]

class DragOutput(DragGate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic_gate = Output()
        self.states = {1:"Images/GateIcons/output_on.png", 0:"Images/GateIcons/output_off.png", None:"Images/GateIcons/output_empty.png"}
        self.update_state()

    
    def update_state(self):
        self.img.source = self.states[self.logic_gate.getOutput()]


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
        self.ids["toolLabel"].text = 'move'
        self.ids["connectToggle"].state = "normal"
        self.ids["disconnectToggle"].state = "normal"
        self.ids["moveToggle"].state = "down"

    def addGateToCanvas(self, gate_type):
        self.ids["gateCanvas"].addGate(gate_type)
        
kv = Builder.load_file("test.kv")

class LogicGateSimulator(App):
    def build(self):
        #self.icon = "Images/Me.jpg"
        return MainWindow()

if __name__ == '__main__':
    LogicGateSimulator().run()
