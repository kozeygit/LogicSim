## Kivy GUI ##
import kivy, os, sys
kivy.require('1.0.1')
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior

class ExitPopup(Popup):
    def closeWindow(self):
        sys.exit()


class MainWindow(Widget):
    gateCanvas = ObjectProperty(None)

    def addGateToCanvas(self, *args):
        self.gateCanvas.addGate()


class GateCanvas(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

#     def on_touch_down(self, touch):
# # if the touch is not for me, and if i don't want to use it, avoid it.
#         if not self.collide_point(*touch.pos):
#             return
#         print("WOOOO")
#         self.root.ids[Board].addGate()

    def addGate(self, *args):
        print("hello")
        self.add_widget(Gate())
        print(self.children)

class GateButton(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def addGateToCanvas(self, *args):
        print(self)
        self.ids(args)

class Gate(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "Images/GateIcons/and.png"
        self.size = 200,200
        self.size_hint = 0.5, 0.5


kv = Builder.load_file("test.kv")

class LogicGateSimulator(App):
    def build(self):
        #self.icon = "Images/Me.jpg"
        return MainWindow()

if __name__ == '__main__':
    LogicGateSimulator().run()
