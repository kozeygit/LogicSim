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

class MainWindow(Widget):
    def closeWindow(self):
        sys.exit()

class GateButton(Widget):
    pass

class LogicGate(Widget):
    def __init__(self, **kwargs):
        pass

class MyLayout(Widget):
    pass

kv = Builder.load_file("test.kv")

class TheApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    TheApp().run()
