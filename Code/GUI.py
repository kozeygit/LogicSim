## Kivy GUI ##
import kivy, os, sys
kivy.require('1.0.1')
from kivy.app import App
from kivy.uix.image import Image
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

class MainWindow(Widget):
    pass

class ExitPopup(Popup):
    def closeWindow(self):
        sys.exit()

class Gate(Button):
    def __init__(self, **kwargs):
        super(Gate, self).__init__(**kwargs)

class GateCanvas(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

#     def on_touch_down(self, touch):
# # if the touch is not for me, and if i don't want to use it, avoid it.
#         if not self.collide_point(*touch.pos):
#             return
#         print("WOOOO")
#         self.root.ids[Board].addGate()


    def addGate(self):
        img = Image(source="Images/GateIcons/and.png")
        self.add_widget(img)

class GateButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def addGateToBoard(self):
        print("Hello")
        self.root.ids["Board"].addGate()

class LogicGate(Widget):
    pass

class MyLayout(Widget):
    pass

kv = Builder.load_file("test.kv")

class LogicGateSimulator(App):
    def build(self):
        #self.icon = "Images/Me.jpg"
        return MainWindow()

if __name__ == '__main__':
    LogicGateSimulator().run()
