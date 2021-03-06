import kivy
kivy.require('1.7.2')
 
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Canvas
from functools import partial
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput

import sys
from random import *
 
#graphics
from kivy.config import Config
Config.set('graphics','resizable',0)
from kivy.core.window import Window;
Window.clearcolor = (0,0,0,1.)


class Paradigm_Base(Widget):
    '''
    Main parent class for paradigms to be implemented. To preserve style and interfaces
    this class is used for all menu and button functions for all paradigms, and then inherited by other
    classes to extend.
    You can add as many buttons in this menu as you want, and each is identified by its
    text string.

    parameter:
    inherits from Widget, as in Kivy syntaxthismodule thismodule 
    '''

    buttonList = []
 
    def __init__(self, **kwargs):
        #create custom event to interact with parent and child instances. Kivy has events but here 
        #we make our own.

        #first we make an event, then we add the event to the button.
        #Our new event we call 'on_button_release'

        #Second we need to define the function again for the dispatcher (so there is no 'unkown' error), with no content,
        #'on_button_release' (see below)

        #Third we need to also define a connected custom_callback function, which
        #does what we want to do when the callback comes.
        #then we send the new custom_callback function to the dispatcher, 
        #which completes the creating of a new callback.

        #Fourth we add buttons to the menu (addButtons), we link our new custom_callback to each button, linked with 
        #the 'on_release' flag, which is what is to be done when a button is released.
    
        self.register_event_type('on_button_release')  
        super(Paradigm_Base, self).__init__(**kwargs)
        #basic parameters that can be overwritten in child class
        self.menu_color = [.8, .8, 1, .9]
        self.menu_color_letters = [0.4, .4, 0.4, .9]
        self.layout = BoxLayout(orientation = 'vertical')
        self.layout.width = Window.width/2
        self.layout.height = Window.height/2
        self.layout.x = Window.width/2 - self.layout.width/2
        self.layout.y = Window.height/2 - self.layout.height/2
        self.data_from_paradigm = []
        self.add_widget(self.layout)


        #these settings are what can be changed in the Paradigm Setup
        paradigm_setup_values = {
            'total trials': 100,
            'water reward(s)': 0.01,
            'reward pulses': 1,
            'start difficulty': 0,
            'input ignored(s)':0,
            'penalty(s)':5,
            'interval(s)': 2,
            'timout(s)': 10,
            'repeat one side': 0
            }

 
    def on_button_release(self, *args):
        #this needs to be implemented for the kivy dispatcher if we make custom events, but is empty
        pass

    def do_on_release(self):
        #to be used by children
        pass
 
    def custom_callback(self,instance):
        #this is the function that gets called from below bind(on_release).
        #it contains a string with the button text in instance.text, which we will bind to the button
        #so when a button is pressed, we will know by the string which button it was
        self.buttonText = instance.text
        #now we add another function which will get called when button is pressed. We cauld add all the
        #things here, but it is cleaner to have one empty function to be inherited and customized later
        self.do_on_release()
        #now we send our new event with its name to the dispatcher
        self.dispatch('on_button_release') 

    


    def clear_screen(self, instance):
        self.parent.canvas.clear()
        self.remove_widget(self.layout)
     
    def start_new(self,instance):
        self.clear_screen(instance)
        print 'starting'
         
    def addButtons(self):
        #now add as many buttons as you like
        for button_text_label in self.buttonList:
            temp_button = MyButton(text = button_text_label)
            #if these two colors are not redefined in the inherited class, the default is used
            temp_button.color = self.menu_color_letters
            temp_button.background_color = self.menu_color
            #when the button is released the custom_callback function is called
            temp_button.bind(on_release = self.custom_callback) 
            self.layout.add_widget(temp_button)

    def give_reward(self):
        print 'water..'
 
    def buildUp(self):
        self.addButtons()
     





class Start_Screen(Widget):
    '''
    Start screen that shows two options buttons to start new paradigm or load previous.
    '''
   
    def __init__(self, **kwargs):
        super(Start_Screen, self).__init__(**kwargs)
        
        #add background color and text
        with self.canvas.before:
            Color(1,0,0,0.5)
            Rectangle(pos=(Window.width*0.1,  Window.height*0.2),
                    size=(Window.width*0.8, Window.height*0.4))
            t = Label(text="Welcome, please choose", color = (1,1,0,1), pos=(Window.width*0.1,  Window.height*0.3),
                    size=(Window.width*0.8, Window.height*0.4), font_size = 48)
            #somehow below is required or the first buttons do not expand
            w = Label(text='')

        self.layout =FloatLayout()
        self.layout.width = Window.width*0.7
        self.layout.height = Window.height*0.7
        self.layout.x = Window.height*0.3
        self.layout.y = Window.width*0.1
        self.add_widget(self.layout)

        #now add text and buttons, in relation to the float layout
        start_button = Button(text='Start new paradigm',   size_hint=(.3, .2),
                pos_hint={'x':.005, 'y':.2})
        start_button.bind(on_press= self.start_new)
 
        continue_button = Button(text='Continue previous', size_hint=(.3, .2),
                pos_hint={'x':.5, 'y':.2})
        continue_button.bind(on_press= self.continue_prev)

        self.layout.add_widget(start_button)
        self.layout.add_widget(continue_button)

    def clear_screen(self, instance):
        self.parent.canvas.clear()
        self.remove_widget(self.layout)
        self.sm2 = TopMenu()
        self.sm2.buildUp()
        self.parent.add_widget(self.sm2)

    def start_new(self,instance):
        self.clear_screen(instance)
        print 'new'
         
    def continue_prev(self, instance):
        self.clear_screen(instance)
        print 'cont'





class TopMenu(Paradigm_Base):
    '''
    This is the widget for the top menu. The buttons that are displayed are 
    defined in Button list. Each of those buttons has a drop down list of 
    further buttons, defined in menu_items.
    
    To add a new paradigm, add the paradigm name to the 'button_text_label' list.
    Also create a new .py module with the exact name without whitespace of what you entered in the list
    as the main function that gets executed first.

    Then use that as the .py name, but add 'Paradigm_' in front.

    Example:
    #your paradigm added to List
        paradigmList = ['Two Images']
    #the py file that has all the paradigm functions
        Paradigm_TwoImages.py
    #the first function in that py file
        def TwoImages()
  


    This class inherits from the Paradigm_Base class.

    parameter:
    inherits from Paradigm_Base
    '''
    #setup the menu button names, inherit from above
    buttonList = ['Choose Paradigm', 'Paradigm Setup', 'Show Data', 'Pause/Stop', 'Copy data to USB']
    
    def __init__(self, **kwargs):
        super(TopMenu, self).__init__(**kwargs)
        #overwrite the basic layout from parent class
        self.layout_top_menu = BoxLayout(orientation = 'horizontal')
        self.layout_top_menu.width = Window.width
        self.layout_top_menu.height = Window.height*0.05
        self.layout_top_menu.x = 0
        self.layout_top_menu.y =  self.layout_top_menu.height*19
        self.add_widget(self.layout_top_menu)
        self.menu_color = [.8, .7,0, .9]
        self.menu_color_letters = [0.8, 1, 1, 1]
        self.temp_val_setting = 0

        self.paradigmList = ['Two Images', 'MIRCs']

        self.menu_items = {
                        0: self.paradigmList,
                        1: [' - '],
                        2: ['Plot Performance', 'Plot Responses'],
                        3: ['Pause', 'Continue','Abort'],
                        4: ['Copy to USB']}
     

        self.paradigm_setup_values = {
            'total trials': 100,
            'water reward(ms)': 10,
            'reward pulses': 1,
            'start difficulty': 0,
            'input ignored(s)':0,
            'penalty(s)':5,
            'interval(s)': 2,
            'timout(s)': 10,
            'repeat one side': 0
            }

        self.paradigm_setup_value_ranges = {
            'total trials': [0, 1000],
            'water reward(s)': [0, 1000],
            'reward pulses': [1,5],
            'start difficulty': [0, 1.0],
            'input ignored(s)':[0,10],
            'penalty(s)':[0, 40],
            'interval(s)': [0, 40],
            'timout(s)': [0,40],
            'repeat one side': [0,50]
            }
  
    def addButtons(self):
        for i, button_text_label in enumerate(self.buttonList):
            temp_button = MyButton(text = button_text_label)
            #if these two colors are not redefined in the inherited class, the default is used
            temp_button.color = self.menu_color_letters
            temp_button.background_color =  [.8, .7,0, .9]
            #now add dropdown buttons
            dropdown = DropDown()
            #if in parameter settings, combine dict to string
            if i is 1:
                for y in self.paradigm_setup_values:
                    submenu_string = y+': '+str(self.paradigm_setup_values[y])
                    btn = Button(text=submenu_string, size_hint_y=None, height=44)
                    btn.background_color =  [.8, .9,.7, .9]
                    btn.bind(on_release=lambda btn: dropdown.select(btn.text))
                    dropdown.add_widget(btn)
            else:
                for submenu_string in self.menu_items[i]:
                    # when adding widgets, we need to specify the height manually (disabling
                    # the size_hint_y) so the dropdown can calculate the area it needs.
                    btn = Button(text=submenu_string, size_hint_y=None, height=44)
                    btn.background_color =  [.8, .9,.7, .9]
                    # for each button, attach a callback that will call the select() method
                    # on the dropdown. We'll pass the text of the button as the data of the
                    # selection.
                    btn.bind(on_release=lambda btn: dropdown.select(btn.text))
                    #then add the button inside the dropdown
                    dropdown.add_widget(btn)
            #bind the dropdown to the main menu button
            temp_button.bind(on_release = dropdown.open) 
            dropdown.bind(on_select=lambda instance, x: self.menu_function_handler(x))
            #get info about what has been pressed
            #dropdown.bind(on_select=lambda instance, x: setattr(temp_button, 'text', x))
            self.layout_top_menu.add_widget(temp_button)
 

    #call the function matching the string (make sure the name exist, without space)
    def menu_function_handler(self,button_text_label):
        #thismodule = sys.modules[__name__]
        #this will call the external module for paradigm.
        #The module needs to start with Paradgim_ and have the same name as the button
        #text without whitespace. The main function must also be the same name without
        #whitespace.

        #if the button is a paradigm, go to corresponding module function
        if button_text_label in self.paradigmList:
            #before we start it we show the start screen
            self.paradigm_start_screen() 
            #dynamically import the py module requested (eg Paradigm_TwoImages.py)
            button_name = button_text_label.replace(" ", "")
            m = __import__ ('Paradigm_'+button_name)
            #get the function with the name without Paradigm_ (eg TwoImages.py)
            func = getattr(m,button_name)
            #call the function which initialized the paradigm class and return the class instance
            self.current_paradigm = func()
            #now that we have the class in this workspace we can use it and call the other functions
            self.current_paradigm.buildUp()
            self.parent.add_widget(self.current_paradigm)
            #function()
        else:
            #if paradigm setting is pressed
            name_only = button_text_label.rsplit(':', 1)[0]
            value_only = int(button_text_label.rsplit(':', 1)[1])
            min = self.paradigm_setup_value_ranges[name_only][0]
            max = self.paradigm_setup_value_ranges[name_only][1]
            if name_only in self.paradigm_setup_values:
                self.get_user_value(name_only, value_only, min, max)
                #update the field 
                self.paradigm_setup_values[name_only] = self.temp_val_setting
                print self.temp_val_setting
            self.update_menu_button()
    

    def get_user_value(self, button_text, current_val, min_, max_):
        
        #make label with current value
        l = Label(text=str(current_val), color = (1,1,0,1), font_size = 40)
        #make slider for popup
        s = Slider(min=min_, max=max_, value=self.temp_val_setting)
        #update value
        def on_slider_move(instance,value):
            l.text = str(int(value))
            self.temp_val_setting = int(value)
            
        s.bind(value=on_slider_move)

        #make button for popup
        content = Button(text='Change Parameter '+button_text, background_color=(0, 1, 0, .5),font_size = 20)
        box = BoxLayout(orientation = 'vertical')
        box.add_widget(l)
        box.add_widget(s)
        box.add_widget(content)
        popup = Popup(title ='Please set new value for '+button_text, content=box, pos_hint={'x': 0,'y':0},  
            size_hint=(None, None), size=(Window.width, Window.height*0.95))
        content.bind(on_press=popup.dismiss)
        popup.open()   

    def OnSliderValueChange(self):
        pass

    def update_menu_button(self):
        self.remove_widget(self.layout_top_menu)
        self.layout_top_menu = BoxLayout(orientation = 'horizontal')
        self.layout_top_menu.width = Window.width
        self.layout_top_menu.height = Window.height*0.05
        self.layout_top_menu.x = 0
        self.layout_top_menu.y =  self.layout_top_menu.height*19
        self.add_widget(self.layout_top_menu)
        self.menu_color = [.8, .7,0, .9]
        self.menu_color_letters = [0.8, 1, 1, 1]

        self.paradigm_setup_values['total trials'] = 200
        self.addButtons()



    def clear_start_screen(self, instance):
        self.remove_widget(self.layout_start)
        #self.remove_widget(self.txt_start)
        #self.remove_widget(self.layout_start)


    def paradigm_start_screen(self):
        
        #add background color and text
        #with self.canvas.before:
        #    Color(1,1,0,0.5)
        #    self.bg_start =  Rectangle(pos=(Window.width*0.1,  Window.height*0.2),
        #            size=(Window.width*0.8, Window.height*0.4))
        #    self.txt_start = Label(text="Press start to start paradigm", color = (1,0.7,0,0.7), pos=(Window.width*0.1,  Window.height*0.3),
        #            size=(Window.width*0.8, Window.height*0.4), font_size = 48)
        #    #somehow below is required or the first buttons do not expand
        #    w = Label(text='')

        #make new float layer
        self.layout_start =FloatLayout()
        self.layout_start.width = Window.width*0.7
        self.layout_start.height = Window.height*0.7
        self.layout_start.x = Window.height*0.3
        self.layout_start.y = Window.width*0.1
        self.add_widget(self.layout_start)

        #add button to layer
        paradigm_start_button = Button(text='Start',   size_hint=(.2, .2),
                pos_hint={'x':.28, 'y':.2})
        paradigm_start_button.bind(on_press= self.clear_start_screen)
        self.layout_start.add_widget(paradigm_start_button)

        #add text to layer
        self.txt_start = Label(text="Press start to start paradigm", color = (1,0.7,0,0.7), pos=(Window.width*0.14,  Window.height*0.3),
                    size=(Window.width*0.8, Window.height*0.4), font_size = 48)
        self.layout_start.add_widget(self.txt_start)
      
  



class MyButton(Button):
    '''
    Class used to style the buttons uniformly. Inherits from kivy Button Class and 
    overwrites a few parameters

    parameter:
    inherits from Widget, as in Kivy syntaxthismodule thismodule 
    '''
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.font_size = Window.width*0.018


class GUI(Widget):
    '''
    Main widget that runs the whole thing and the primary object.
    '''
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
 
     
        build_version = '0.4'
        self.version_build = Label(text = build_version, color=[1,0,0,1])
        self.add_widget(self.version_build)

    #handle touch anywhere but button
    def on_touch_down(self, touch):
        print 'touched outside button'

  
 
class ClientApp(App):
    '''
    The first class called and creates a handle to the root in the hierarchy
    '''
    def build(self):
        #root widget
        self.parent = Widget() #
        self.app = GUI()
        #show start screen
        self.s_screen = Start_Screen()
        self.parent.add_widget(self.s_screen)
        #use this hierarchy to make it easy to deal with buttons
        self.parent.add_widget(self.app) 
      
        return self.parent
 
if __name__ == '__main__' :
    ClientApp().run()