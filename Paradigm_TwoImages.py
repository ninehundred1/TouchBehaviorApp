#!/usr/bin/python
# Filename: Touch_Training_menus_classes.py
from TouchTraining import Paradigm_Base


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

import sys
from random import *
import time
 
#graphics
from kivy.config import Config
Config.set('graphics','resizable',0)
from kivy.core.window import Window;
Window.clearcolor = (0,0,0,1.)




class Paradigm_Two_choice_images(Paradigm_Base):
    '''
    Paradigm that shows two images from file, with a button underneath the image.
    When the right button is clicked, there is a water reward.
    Correct and incorrect presses are stores to be analyzed for performance.

    This class inherits from the main menu class and sets the choice buttons
    as well as adds an image as the stimulus.
    Further functionality is added

    parameter:
    inherits from Paradigm_Base
    '''
    #the buttons we want
    buttonList = ['left', 'right']
 
    def __init__(self, **kwargs):
        super(Paradigm_Two_choice_images, self).__init__(**kwargs)
        #overwrite the basic layout from parent class
        self.layout = BoxLayout(orientation = 'horizontal')
        self.layout.width = Window.width
        self.layout.height = Window.height/8
        self.layout.x = 0
        self.layout.y = 0
        self.add_widget(self.layout)

        #empty images to init
        self.stim_left =  Widget()
        self.stim_right =  Widget()
        self.image_correct = Image(source = 'correct_l.jpg')
        self.image_wrong = Image(source = 'wrong_l.jpg')
        self.stimulus_is_left = 1

        #initi data class
        self.data = Data_Class()

        #init preview
        self.prev_string = Label(text = '-no stats yet-', color=[1,0,0,1])
        self.prev_string.y = Window.height*0.85
        self.prev_string.x = Window.width*0.4
        self.add_widget(self.prev_string)

        #init other stuff
        self.penalty = 2
        self.interval = 1
        self.reward_time = 1
        self.last_was_correct = 0


        #start timer
        self.start_time = time.clock()


    #Do deal with events and with timing the processes, below
    #is a chronolical order of what happens after trial.
    #To pause kivy you need to use clock schedule in between the timeline

    #what happen if a button is pressed
    def do_on_release(self):
        choice = self.buttonText
        self.remove_widget(self.stim_left)
        self.remove_widget(self.stim_right)
        self.after_choice(choice)


    def after_choice(self,choice):
        self.process_response(choice)
        self.show_data_preview()
        #sequence will move on in process_response
       
        


    #here you can pause the app without freezing it using clock to when to proceed to 
    # next call
    def wait_interval(self, dt):
        if not self.last_was_correct:
            popup_text = 'wrong - waiting for penalty delay and interval...'
            self.block_screen(popup_text, self.penalty+self.interval, self.start_next)
        else:   
            popup_text = 'correct - waiting for interval...'
            self.block_screen(popup_text, self.interval, self.start_next)
        


    def block_screen(self, message, time, function_to_call):
        popup = Popup(title= message, pos_hint={'x': 0, 
                            'y':0},  
            size_hint=(None, None), size=(Window.width, Window.height*0.95))
        popup.open()
        #time the closing
        Clock.schedule_once(popup.dismiss, time)
        #time the continue to be right after the closing
        Clock.schedule_once(function_to_call, time)


    def block_screen_initialize(self, button_text, message):
        content = Button(text=button_text,  pos_hint={'x': 800,'y':0},  
            size_hint=(None, None), size=(Window.width*0.96, Window.height*0.14))
        popup = Popup(title = message, content=content, pos_hint={'x': 0,'y':0},  
            size_hint=(None, None), size=(Window.width, Window.height*0.95))
        content.bind(on_press=popup.dismiss)
        popup.open()


    def start_next(self, dt):
        self.choose_side()
        self.set_stimulus_images()
        #display what the last trial was
        message_middle = 'LAST TRIAL '+['WRONG -- ', 'CORRECT -- '][self.last_was_correct == 1]
        #also show current stats preview in initialize screen
        message_end = self.data.make_preview_string()
        self.block_screen_initialize('Initialize Trial Here', message_middle+message_end)


    def process_response(self, choice):
        #log time
        self.data.all_times.append(time.clock() - self.start_time)
        #increment trial number
        self.data.total_trials += 1
        #add what side stimulus was on (stimulus_is_left =1 means was left, 0 is right)
        self.data.all_sides_stimuli.append(self.stimulus_is_left)
        #if choice was left
        if choice is 'left':
            #1 means animal made choice to left
            self.data.all_sides_reponses.append(1)
            #if stimulus was left
            if self.stimulus_is_left:
                self.data.left_correct += 1
                #3 means correct choice made
                self.data.all_responses.append(3)
                self.last_was_correct = 1
                
            else:
                #2 means wrong choice made
                self.data.all_responses.append(2)
                self.data.left_wrong += 1
                self.last_was_correct = 0

        elif choice is 'right':
            self.data.all_sides_reponses.append(0)
            #if right was correct
            if not self.stimulus_is_left:
                self.data.right_correct += 1
                self.data.all_responses.append(3)
                self.last_was_correct = 1
               
            else:
                self.data.all_responses.append(2)
                self.data.right_wrong += 1
                self.last_was_correct = 0
        #if timeout
        elif choice is 'timeout':
            self.data.timeouts += 1
            self.data.all_responses.append(1)
            self.last_was_correct = 1

        #move on along trial here    
        self.give_reward(self.reward_time)

    def give_reward(self, time_open):
        if self.last_was_correct:
            self.block_screen('CORRECT - Giving reward', time_open, self.wait_interval)
        else:
            self.wait_interval('')


    def show_data_preview(self):
        new_prev_string = self.data.make_preview_string()
        self.prev_string.text = new_prev_string

 
    def choose_side(self):
        self.stimulus_is_left = randint(0,1)

    def set_stimulus_images(self):
        image_size_y = Window.height
        image_size_x = Window.width*0.7
        if self.stimulus_is_left == 1:
            #left
            self.stim_left = self.image_correct
            self.stim_left.size = (image_size_y,image_size_x)
            self.stim_left.pos = (-Window.width*0.1, 10)
            self.stim_left.opacity = 1
            #right
            self.stim_right = self.image_wrong
            self.stim_right.size = (Window.height*2,Window.height)
            self.stim_right.pos = (0, 0)
            self.stim_right.opacity = 1
        else:
            #left
            self.stim_right = self.image_wrong
            self.stim_right.size = (image_size_y,image_size_x)
            self.stim_right.pos = (-Window.width*0.1, 10)
            self.stim_right.opacity = 1
            #right
            self.stim_left = self.image_correct
            self.stim_left.size = (Window.height*2,Window.height)
            self.stim_left.pos = (0, 0)
            self.stim_left.opacity = 1
       
        self.add_widget(self.stim_left)
        self.add_widget(self.stim_right)

    ##add start screen before start
    #def buildUp(self):
    #    self.addButtons()
    #    self.block_screen_initialize('Initialize Trial Here', 'STARTING SESSION')
    
    def start_new(self):
        self.block_screen_initialize('Initialize Trial Here', 'STARTING SESSION')

    def clear_start_screen(self, instance):
        self.remove_widget(self.layout_start)
        self.block_screen_initialize('Initialize Trial Here', 'STARTING SESSION')



class Data_Class(object):
    def __init__(self):
        #data 
        self.total_trials = 0
        self.left_correct = 0
        self.right_correct = 0
        self.left_wrong = 0
        self.right_wrong = 0
        self.timeouts = 0
        #1 = timeout, 2 = wrong, 3 = correct
        self.all_responses = []
        #1 = left, 0 = right
        self.all_sides_reponses = []
        #1 = left, 0 = right
        self.all_sides_stimuli = []
        #times for above
        self.all_times = []

    def make_preview_string(self):
        '''
        make preview string for display
        trial:
        rewards:
        lft:
        rgt:
        last10binCorr%:
        totalCorr%
        '''
        trial = self.total_trials
        rewards = self.left_correct+self.right_correct
        left = self.all_sides_reponses.count(1)
        right = self.all_sides_reponses.count(0)
        #bin last 50 values
        correct_wrong = filter(lambda x: x==2 or x==3, self.all_responses)
        #replace correct(3) with 1 and wrong(2) with 0 for average 
        correct_wrong = [1 if x==3 else x for x in correct_wrong]
        correct_wrong = [0 if x==2 else x for x in correct_wrong]
        
        last10binCorr = self.bin_range(correct_wrong, 10)
        preview_string = 'trial: %s - rewards: %s - left pokes: %s - right pokes: %s - last 5 bins of 10: %s' %(
            trial, rewards, left, right, last10binCorr)
        return preview_string


    def bin_range(self, list_in, range):
        #round down to nearest bin
        to_be_binned =list_in[0: len(list_in) - (len(list_in) % range)]
        start_index = 0
        end_index = range
        list_of_bins = []
    
        #list_of_errors = []
        while end_index <= len(to_be_binned):
            list_of_bins.append(
                reduce(lambda x, y: x + y, to_be_binned[start_index:end_index]) / float(len(to_be_binned[start_index:end_index])))
            #list_of_errors.append(error(list_in[start_index:end_index]))
            start_index += range
            end_index += range 
        return list_of_bins


       

#create class and then return to main program to be bound to buttont
#add all data to data_from_paradigm which is defined in main class
def TwoImages():    
    current_paradigm = Paradigm_Two_choice_images()
    return current_paradigm


   
version = '0.1'


# End of Touch_Training_menus_classes.py
			