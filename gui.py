import kivy
from kivy.uix.dropdown import DropDown
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from  kivy.uix.switch import Switch
import os
from kivy.config import Config
from kivy.uix.spinner import Spinner
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1
        self.inside = GridLayout()
        self.inside.padding = 10
        self.inside.spacing = 5
        self.inside.cols = 2
        # self.spinner = Spinner(
        # # default value shown
        # text='View',
        # # available values
        # values=('Home', 'Settings', 'File Manager'),
        # # just for positioning in our example
        # size_hint=(None, None),
        # size=(100, 44),
        # pos_hint={'center_x': .5, 'center_y': .5})
        #
        # self.spinner.background_color = 0, 1, 0
        # self.add_widget(self.spinner)



        # self.inside.add_widget(Label(text="Enter Cable #: ",font_size=20))
        # self.number = TextInput(multiline=False)
        # self.inside.add_widget(self.number)



        popup = Popup(title='Configure',
        size_hint=(None, None), size=(500, 500))

        box = GridLayout(row_default_height=50,row_force_default=True)
        box.padding = 10
        box.spacing = 5
        box.cols = 2
        box.add_widget(Label(text='Enter Cable #'))
        cableInput = TextInput(multiline=False)
        cableInput.bind(on_text_validate=self.on_enter)
        box.add_widget(cableInput)


        box.add_widget(Label(text='Select Cable Type'))
        spinner = Spinner(
        # default value shown
        text='',
        # available values
        values=('T1', 'T2', 'T3'),
        # just for positioning in our example
        size_hint=(0.3, 0.2),
        pos_hint={'x': .35, 'y':.75})
        spinner.bind(text=self.show_selected_value)

        box.add_widget(spinner)
        g = GridLayout(cols=2, row_force_default=True, row_default_height=40)
        g.padding = 5
        g.spacing = 50
        submit = Button(text='Submit',font_size=20,size_hint_x=None, width=200)
        submit.background_color = 0, 1, 0, 1
        submit.bind(on_release= lambda x: self.runTest())
        submit.bind(on_release= lambda x: popup.dismiss())
        submit.bind(on_release = self.pop)
        submit.bind(on_release = self.puopen)
        g.add_widget(submit)
        reset = Button(text='Reset',font_size=20,size_hint_x=None, width=200)
        g.add_widget(reset)

        box.add_widget(g)


        popup.add_widget(box)


        self.start = Button(text='Start Test',font_size=20)
        self.start.bind(on_release= lambda x: popup.open())
        self.inside.add_widget(self.start)

        self.add_widget(self.inside)


        self.progress_label = Label(text="Progression: ",font_size=20)

        self.add_widget(self.progress_label)

        self.progress_bar = ProgressBar()
        self.progress_bar.padding = 10
        self.progress_bar.spacing = 5
        self.add_widget(self.progress_bar)


    def on_enter(instance, value):
        print('Cable Serial #', value.text)

    def show_selected_value(spinner, text,instance):
        print('The Cable type selected is ', text.text)


    # the function which works when you clicj = k the button
    def pop(self, instance):
        self.progress_bar.value = 1


    # To continuesly increasing the value of pb.
    def next(self, dt):

        self.progress_label.text = "Testing in progress :" + str(self.progress_bar.value)
        if self.progress_bar.value>= 100:
            self.progress_label.text = "Testing complete :" + str(self.progress_bar.value)
            return False
        self.progress_bar.value += 1

    def puopen(self, instance):
        Clock.schedule_interval(self.next, 4/5)

    #def toggleSubmitButton(self):



    def runTest(self):
        print("HELLO")

        #os.system('python AutomationScript.py')


    def createDropDownMenu(self):
        # create a dropdown with 10 buttons
        dropdown = DropDown()
        # When adding widgets, we need to specify the height manually
        # (disabling the size_hint_y) so the dropdown can calculate
        # the area it needs.
        btn = Button(text='Type 1', size_hint_y=None, height=44)

        # for each button, attach a callback that will call the select() method
        # on the dropdown. We'll pass the text of the button as the data of the
        # selection.
        btn.bind(on_release=lambda btn: dropdown.select(btn.text))

        # then add the button inside the dropdown
        dropdown.add_widget(btn)

        btn = Button(text='Type 2', size_hint_y=None, height=44)

        btn.bind(on_release=lambda btn: dropdown.select(btn.text))

        dropdown.add_widget(btn)


        btn = Button(text='Type 3', size_hint_y=None, height=44)

        btn.bind(on_release=lambda btn: dropdown.select(btn.text))

        dropdown.add_widget(btn)

        mainbutton = Button(text='',font_size=20)


        mainbutton.bind(on_release=dropdown.open)


        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        return mainbutton


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    Config.set('kivy', 'keyboard_mode', 'system')
    MyApp().run()
