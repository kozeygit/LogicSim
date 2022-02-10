## Kivy GUI ##
import kivy, os, sys
kivy.require('1.0.1')
from kivy.app import App
from kivy.uix.image import Image
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup

class MainWindow(Widget):
    pass

class ExitPopup(Popup):
    def closeWindow(self):
        sys.exit()

class Gate(Widget):
    pass

class GateButton(Widget):
    pass

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
