## Kivy GUI ##
import kivy
kivy.require('1.0.1')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

class MyGridLayout(Widget):

    def press(self, instance):
        name = self.name.text
        pizza = self.pizza.text

        self.top_grid.add_widget(Label(text=f"Hello {name}, you like {pizza} pizza!"))
        print(f"Hello {name}, you like {pizza} pizza!")

        self.name.text = ""
        self.pizza.text = ""



class TestApp(App):
    def build(self):
        return MyGridLayout()


if __name__ == '__main__':
    TestApp().run()
