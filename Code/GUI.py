## Kivy GUI ##
import kivy
kivy.require('1.0.1')
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class LogicGate(Widget):
    def __init__(self, **kwargs):
        pass


class MyGridLayout(Widget):
    name = ObjectProperty(None)
    pizza = ObjectProperty(None)
    colour = ObjectProperty(None)

    def press(self):
        name = self.name.text
        pizza = self.pizza.text
        colour = self.colour.text

        #self.top_grid.add_widget(Label(text=f"Hello {name}, you like {pizza} pizza!"))
        print(f"Hello {name}, you like {pizza} pizza!")

        self.name.text = ""
        self.pizza.text = ""
        self.colour.text = ""



class TestApp(App):
    def build(self):
        return FloatLayout()


if __name__ == '__main__':
    TestApp().run()
