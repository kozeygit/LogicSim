## Kivy GUI ##
import kivy, os, sys
kivy.require('2.0.0')
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from logic.board import Board
from logic.gates import *

Window.size = (400, 500)

class ExitPopup(Popup):
    def closeWindow(self):
        sys.exit()



class GateCanvas(ScatterLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = Board()
        gate_dict = {
            "and":[],
            "or":[],
            "not":[],
            "xor":[],
            "input":[],
            "output":[],
            "clock":[],
            
        }

    def on_touch_down(self, touch):
# if the touch is not for me, and if i don't want to use it, avoid it.
        if not self.collide_point(*touch.pos):
            return
        print("Touchy")

    def addGate(self, gate_type):
        print("Working", gate_type)


class GateButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DragGate(DragBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "Images/GateIcons/and.png"
        self.allow_stretch = True
        self.size_hint = None, None
        self.size = (10,10)
        self.pos_hint = {"top":0.5, "x":0}

class DragAndGate(DragGate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "Images/GateIcons/and.png"
        self.pos_hint = {"top":0.5, "x":0}


class MainWindow(Widget):
    gateCanvas = ObjectProperty(None)
    andButton = ObjectProperty(None)
    orButton = ObjectProperty(None)
    xorButton = ObjectProperty(None)
    notButton = ObjectProperty(None)
    Test = "This works?"
    print(gateCanvas)

    def addGateToCanvas(self, gate_type):
        self.ids["gateCanvas"].addGate(gate_type)
        
kv = Builder.load_file("test.kv")

class LogicGateSimulator(App):
    def build(self):
        #self.icon = "Images/Me.jpg"
        return MainWindow()

if __name__ == '__main__':
    LogicGateSimulator().run()
