import kivy
from kivy.uix.dropdown import DropDown
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import os
from kivy.config import Config


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1
        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="Enter Cable #: ",font_size=20))
        self.number = TextInput(multiline=False)
        self.inside.add_widget(self.number)



        self.add_widget(self.inside)
        self.type = self.createDropDownMenu()
        self.add_widget(self.type)

        self.start = Button(text='Start',font_size=20)
        self.start.background_color = .7, .7, 1, 1
        self.start.bind(on_release= lambda x: self.pressed())
        self.add_widget(self.start)

        #would like to add parameters for input to python file (cable #, type)
    def pressed(self):
        os.system('python AutomationScript.py')


    def createDropDownMenu(self):
        # create a dropdown with 10 buttons
        dropdown = DropDown()

        # When adding widgets, we need to specify the height manually
        # (disabling the size_hint_y) so the dropdown can calculate
        # the area it needs.
        btn = Button(text='Cable Type 1', size_hint_y=None, height=44)

        # for each button, attach a callback that will call the select() method
        # on the dropdown. We'll pass the text of the button as the data of the
        # selection.
        btn.bind(on_release=lambda btn: dropdown.select(btn.text))

        # then add the button inside the dropdown
        dropdown.add_widget(btn)

        btn = Button(text='Cable Type 2', size_hint_y=None, height=44)

        btn.bind(on_release=lambda btn: dropdown.select(btn.text))

        dropdown.add_widget(btn)


        btn = Button(text='Cable Type 3', size_hint_y=None, height=44)

        btn.bind(on_release=lambda btn: dropdown.select(btn.text))

        dropdown.add_widget(btn)

        mainbutton = Button(text='Select cable type',font_size=20)


        mainbutton.bind(on_release=dropdown.open)


        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        return mainbutton


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    Config.set('kivy', 'keyboard_mode', 'systemandmulti')
    MyApp().run()
