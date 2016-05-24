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

import Touch_Training_menu_classes

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
        self.num_presses = 0
        self.add_widget(self.layout)
 
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
 
    def buildUp(self):
    #self.colorWindow()
        self.addButtons()




class Start_Screen(Widget):
    '''
    Start screen that shows the options to start new or load previous
 
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

        

        #add float layout
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
        #self.sm.buildUp()
        self.clear_screen(instance)
        print 'new'
        
        
    def continue_prev(self, instance):
        self.clear_screen(instance)
        print 'cont'



    
        


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

        self.left_is_correct = 1
        #self.add_widget(self.stim_left)
        #self.add_widget(self.stim_right)
        #self.msg = Label(text = 'Flappy Ship')
        #self.msg.font_size = Window.width*0.07
        #self.msg.pos = (Window.width*0.45,Window.height*0.75)
        #self.add_widget(self.msg)
       
        

    #what happen if a button is pressed
    def do_on_release(self):
        print self.buttonText
        #self.stim_left.clear_widgets()
        
        self.remove_widget(self.stim_left)
        self.remove_widget(self.stim_right)
        self.set_up_trial()
        self.set_stimulus_images()
        


    def set_up_trial(self):
        self.left_is_correct = randint(0,1)


    def set_stimulus_images(self):
        image_size_y = Window.height
        image_size_x = Window.width*0.7
        print self.left_is_correct
        if self.left_is_correct == 1:
            #left
            print 'here'
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
        


class TopMenu(Paradigm_Base):
    '''
    This is the widget for the top menu. The buttons that are displayed are 
    defined in Button list. Each of those buttons has a drop down list of 
    further buttons, defined in menu_items.
    If a button gets pressed, the function with the same name of the button 
    is called from the module file Touch_Training_menus_classes.py

    This class inherits from the Paradigm_Base class.

    parameter:
    inherits from Paradigm_Base
    '''
#setup the menu button names, inherit from above
    buttonList = ['Choose Paradigm', 'Paradigm Setup', 'Show Data', 'Pause/Stop', 'Copy data to USB']
 
    def __init__(self, **kwargs):
        super(TopMenu, self).__init__(**kwargs)
        #overwrite the basic layout from parent class
        self.layout = BoxLayout(orientation = 'horizontal')
        self.layout.width = Window.width
        self.layout.height = Window.height*0.05
        self.layout.x = 0
        self.layout.y =  self.layout.height*19
        self.add_widget(self.layout)
        self.menu_color = [.8, .7,0, .9]
        self.menu_color_letters = [0.8, 1, 1, 1]

        self.menu_items = {
                        0: ['Two Images', 'Mirc'],
                        1: ['Interval', 'Penalty'],
                        2: ['Plot Performance', 'Plot Responses'],
                        3: ['Pause', 'Continue','Abort'],
                        4: ['Copy to USB']}
                            
     
  
    def addButtons(self):
        #now add as many buttons as you like
        for i, button_text_label in enumerate(self.buttonList):
            temp_button = MyButton(text = button_text_label)
            #if these two colors are not redefined in the inherited class, the default is used
            temp_button.color = self.menu_color_letters
            temp_button.background_color =  [.8, .7,0, .9]
            #now add dropdown buttons
            dropdown = DropDown()
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
            self.layout.add_widget(temp_button)
 
    #call the function matching the string (make sure the name exist, without space)
    def menu_function_handler(self,button_text_label):
        #thismodule = sys.modules[__name__]
        function=getattr(Touch_Training_menu_classes,button_text_label.replace(" ", "")) 
        #this is calling the same function as the name of button. 
        function('aaaaassss')  



 
class WidgetDrawer(Widget):
#This widget is used to draw all of the objects on the screen
#it handles the following:
# widget movement, size, positioning
    def __init__(self, imageStr, **kwargs):
       super(WidgetDrawer, self).__init__(**kwargs)
 
       with self.canvas:
 
           self.size = (Window.width*.002*25,Window.width*.002*25)
           self.rect_bg=Rectangle(source=imageStr,pos=self.pos,size = self.size)
 
           self.bind(pos=self.update_graphics_pos)
           self.x = self.center_x
           self.y = self.center_y
           self.pos = (self.x,self.y)
           self.rect_bg.pos = self.pos
 
    def update_graphics_pos(self, instance, value):
        self.rect_bg.pos = value
 
    def setSize(self,width, height):
       self.size = (width, height)
 
    def setPos(xpos,ypos):
       self.x = xpos
       self.y = ypos

class WidgetDrawer(Widget):
    #This widget is used to draw all of the objects on the screen
    #it handles the following:
    # widget movement, size, positioning
    #whever a WidgetDrawer object is created, an image string needs to be specified
    #example:    wid - WidgetDrawer('./image.png')
 
    #objects of this class must be initiated with an image string
#;You can use **kwargs to let your functions take an arbitrary number of keyword arguments
#kwargs ; keyword arguments
    def __init__(self, imageStr, **kwargs): 
        super(WidgetDrawer, self).__init__(**kwargs) #this is part of the **kwargs notation
#if you haven't seen with before, here's a link http://effbot.org/zone/python-with-statement.html     
        with self.canvas: 
#setup a default size for the object
            self.size = (Window.width*.002*25,Window.width*.002*25) 
#this line creates a rectangle with the image drawn on top
            self.rect_bg=Rectangle(source=imageStr,pos=self.pos,size = self.size) 
#this line calls the update_graphics_pos function every time the position variable is modified
            self.bind(pos=self.update_graphics_pos) 
            self.x = self.center_x
            self.y = self.center_y
#center the widget 
            self.pos = (self.x,self.y) 
#center the rectangle on the widget
            self.rect_bg.pos = self.pos 
 
    def update_graphics_pos(self, instance, value):
#if the widgets position moves, the rectangle that contains the image is also moved
        self.rect_bg.pos = value  
#use this function to change widget size        
    def setSize(self,width, height): 
        self.size = (width, height)
 #use this function to change widget position    
    def setPos(xpos,ypos):
        self.x = xpos
        self.y = ypos

class ScoreWidget(Widget):
    def __init__(self, **kwargs):
        super(ScoreWidget, self).__init__(**kwargs)
        self.asteroidScore = 0
        self.currentScore = 0
        with self.canvas:
            tmpPos = (Window.width*0.25,Window.height*0.25)
            tmpSize = (Window.width*0.5,Window.height*0.5)
            Color(0.1,.1,.1)
            self.scoreRect = Rectangle(pos= tmpPos,size = tmpSize )
 
    def prepare(self):
        #calculate the score
        try:
 
            self.finalScore = self.asteroidScore*100
 
        except:
            print 'problems getting score'
        self.animateScore()
 
    def animateScore(self):
        #display score at 0 and every time interval add 100 until
        #we reach the final score
        #draw a score widget and schedule updates
        scoreText = 'Score: 0'# + str(self.finalScore)
        self.scoreLabel = Label(text=scoreText,font_size = '20sp')
        self.scoreLabel.x = Window.width*0.3
        self.scoreLabel.y = Window.height*0.3
        self.add_widget(self.scoreLabel)
        Clock.schedule_once(self.updateScore, .1)
        self.drawStars()
 
    def updateScore(self,dt):
        self.currentScore = self.currentScore +100
        self.scoreLabel.text = 'Score: ' + str(self.currentScore)
        if self.currentScore > self.finalScore:
            Clock.schedule_once(self.updateScore, 0.1)
 
    def drawStars(self):
        #0-10 asteroids 0 stars
        #11-50 asteroids 1 star
        #51-200 asteroids 2 stars
        #201-500 asteroids 3 stars
        #501-1000 asteroids 4 stars
        #1001+ asteroids 5 stars
        starNumber = 0
        if self.asteroidScore > 10:
            starNumber = 1
        if self.asteroidScore > 50:
            starNumber = 2
        if self.asteroidScore > 200:
            starNumber = 3
        if self.asteroidScore > 500:
            starNumber = 4
        if self.asteroidScore > 1000:
            starNumber = 5
 
        with self.canvas:
            #draw stars
            #rect one
            starPos = Window.width*0.27, Window.height*0.42
            starSize = Window.width*0.06,Window.width*0.06
            starString = 'gold_star.png'
            if starNumber > 1:
                starString = 'gray_star.png'
            starRectOne = Rectangle(source=starString,pos=starPos, size = starSize)
            #rect two
            starPos = Window.width*0.37, Window.height*0.42
            if starNumber > 2:
                starString = 'gray_star.png'
            starRectTwo = Rectangle(source=starString,pos=starPos, size = starSize)
            #rect three
            starPos = Window.width*0.47, Window.height*0.42
            if starNumber > 3:
                starString = 'gray_star.png'
            starRectThree = Rectangle(source=starString,pos=starPos, size = starSize)
            #rect four
            starPos = Window.width*0.57, Window.height*0.42
            if starNumber > 4:
                starString = 'gray_star.png'
            starRectFour = Rectangle(source=starString,pos=starPos, size = starSize)
            #rect five
            starPos = Window.width*0.67, Window.height*0.42
            if starNumber > 5:
                starString = 'gray_star.png'
                starRectFive = Rectangle(source=starString,pos=starPos, size = starSize)
 
 
class Asteroid(WidgetDrawer):
    #Asteroid class. The flappy ship will dodge these
    imageStr = './sandstone_1.png'
    rect_bg=Rectangle(source=imageStr)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
 
    def move(self):
        self.x = self.x + self.velocity_x
        self.y = self.y + self.velocity_y
 
    def update(self):
        self.move()
 
class Ship(WidgetDrawer):
#Ship class. This is for the main ship object.
#velocity of ship on x/y axis
#setup constants, health, etc
#choose default image:
 
    impulse = 3
    grav = -0.1
 
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    flameSize = (Window.width*.03,Window.width*.03)
 
    def move(self):
        self.x = self.x + self.velocity_x
        self.y = self.y + self.velocity_y
 
    #don't let the ship go too far
        if self.y >  Window.height*0.05:
        #give upwards impulse
            self.impulse = 1
            self.grav = -0.1
 
        if self.y > Window.height*0.95:
            self.impulse = -3
 
    def checkBulletNPCCollision(self,j):
        if self.k.collide_widget(j):
            j.health = j.health - self.k.bulletDamage
            j.attackFlag = 'True'
        #age the bullet
            self.k.age = self.k.lifespan+10
 
    def checkBulletStageCollision(self,q):
        if self.k.collide_widget(q):
            #if object type is asteorid
            try:
                if q.type == 'asteroid':
                    q.health = q.health - self.k.bulletDamage
                    self.k.age = self.k.lifespan+10
            except:
                print 'couldnt hit asteroid'
 
    def determineVelocity(self):
        #move the ship up and down
        #we need to take into account our acceleration
        #also want to look at gravity
        self.grav = self.grav*1.05 #increase gravity
        #set a grav limit
        if self.grav > -4:
            self.grav = -4
#the ship has a propety called self.impulse which is updated
#whenever the player touches, pushing the ship up
#use this impulse to determine the ship velocity
#also decrease the magnitude of the impulse each time its used
 
        self.velocity_y = self.impulse + self.grav
        self.impulse = 0.95*self.impulse


    def drawArrow(self, *largs):
        #draw the arrows directly onto the canvas
        with self.canvas:
            flamePos = (self.pos[0]-Window.width*.02,self.pos[1]+Window.width*.01)
     
            flameRect = Rectangle(source='./flame.png',pos=flamePos, size = self.flameSize)
        #schedule removal
 
    def removeArrows(arrow, *largs):
        self.canvas.remove(arrow)
        Clock.schedule_once(partial(removeArrows, flameRect), .5)
        Clock.schedule_once(partial(self.updateArrows, flameRect), 0.1)
 
    def updateArrows(self,arrow,dt):
        with self.canvas:
            arrow.pos = (arrow.pos[0]-10,arrow.pos[1])
 
            Clock.schedule_once(partial(self.updateArrows, arrow), 0.1)
        return

    def explode(self):
        #create explosion 1
        tmpSize = Window.width*0.25,Window.width*0.2
        tmpPos = (self.x-Window.width*0.095, self.y-Window.width*0.08)
        with self.canvas: #create an explosion image, 
            self.explosionRect = Rectangle(source ='./explosion1.png',pos=tmpPos,size=tmpSize)
        def changeExplosion(rect, newSource, *largs):
            rect.source = newSource
 
        #schedule explosion two
        Clock.schedule_once(partial(changeExplosion, self.explosionRect, './explosion2.png'),0.2)
        #schedule explosion three
        Clock.schedule_once(partial(changeExplosion, self.explosionRect, './explosion3.png'),0.4)
        #schedule explosoin four
        Clock.schedule_once(partial(changeExplosion, self.explosionRect, './explosion4.png'),0.6)
        Clock.schedule_once(partial(changeExplosion, self.explosionRect, './explosion5.png'),0.8)
        def removeExplosion(rect, *largs):
            self.canvas.remove(rect) #remove the explosion drawing
        Clock.schedule_once(partial(removeExplosion, self.explosionRect),1)
 
    def update(self):
        self.determineVelocity()
        self.move()
 


class MyButton(Button):
    #class used to get uniform button styles
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
 #all we're doing is setting the font size. more can be done later
        self.font_size = Window.width*0.018


class GUI(Widget):
#this is the main widget that contains the game. This is the primary object
#that runs
    asteroidList =[]
#important to use numericproperty here so we can bind a callback
#to use every time the number changes
    asteroidScore = NumericProperty(0)
    minProb = 1780
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
 
        #setup label for the score


        build_version = '0.4'
        self.version_build = Label(text = build_version, color=[1,0,0,1])
        self.add_widget(self.version_build)
    
     
 
 
        def check_score(self,obj):
            #update credits
            self.score.text = str(self.asteroidScore)
        self.bind(asteroidScore = check_score)
       
      
 
        #now we create a ship object
        #self.ship = Ship(imageStr = './ship.png')
        #self.ship.x = Window.width/4
        #self.ship.y = Window.height/2
        #self.add_widget(self.ship)
#self.ship.drawArrow()#start the flames
        #Clock.schedule_interval((self.ship.drawArrow), 0.1)
 
    def addAsteroid(self):
        #add an asteroid to the screen
        #self.asteroid
        imageNumber = randint(1,4)
        imageStr = './sandstone_'+str(imageNumber)+'.png'
        tmpAsteroid = Asteroid(imageStr)
        tmpAsteroid.x = Window.width*0.99
 
        #randomize y position
        ypos = randint(1,16)
        ypos = ypos*Window.height*.0625
        tmpAsteroid.y = ypos
        tmpAsteroid.velocity_y = 0
        vel = 55#randint(10,25)
        tmpAsteroid.velocity_x = -0.1*vel
        self.asteroidList.append(tmpAsteroid)
        self.add_widget(tmpAsteroid)
 
    def drawTouchResponse(self,x,y):
        #draw the arrows directly onto the canvas
        with self.canvas:
            tmpSize = Window.width*0.07, Window.width*0.07
            tmpPos = (x-self.width/4,y-self.height/4)
            self.arrowRect = Rectangle(source='./flame1.png',pos=tmpPos, size = tmpSize)
        #schedule removal
        def removeArrows(arrow, *largs):
            self.canvas.remove(arrow)
        def changeExplosion(rect, newSource, *largs):
            rect.source = newSource
        #schedule explosion two
        Clock.schedule_once(partial(changeExplosion, self.arrowRect, './flame2.png'),0.15)
        #schedule explosion three
        Clock.schedule_once(partial(changeExplosion, self.arrowRect, './flame3.png'),0.3)
        #schedule explosoin four
        Clock.schedule_once(partial(changeExplosion, self.arrowRect, './flame4.png'),0.45)
        Clock.schedule_once(partial(removeArrows, self.arrowRect),0.6)
 
    #handle input events
    def on_touch_down(self, touch):
        #self.ship.impulse = 3
        #self.ship.grav = -0.1
        #self.drawTouchResponse(touch.x,touch.y)
        print 'here1'
    def showScore(self):
        #this function will draw the score keeping widget, tabulate the score
        #and rank with stars
        self.scoreWidget = ScoreWidget()
        self.scoreWidget.asteroidScore = self.asteroidScore #pass on score
        self.scoreWidget.prepare()
        self.add_widget(self.scoreWidget)
    def removeScore(self):
        self.remove_widget(self.scoreWidget)
 
    def gameOver(self):
        #add a restart button
        restartButton = MyButton(text='Try Again')
        #restartButton.background_color = (.5,.5,1,.2)
        def restart_button(obj):
            #reset game
            self.removeScore()
 
            for k in self.asteroidList:
                self.remove_widget(k)
                self.ship.xpos = Window.width*0.25
                self.ship.ypos = Window.height*0.5
                self.minProb = 1780
                self.asteroidScore = 0
                self.asteroidList = []
 
            self.parent.remove_widget(restartButton)
            Clock.unschedule(self.update)
            Clock.schedule_interval(self.update, 1.0/60.0)
            restartButton.size = (Window.width*.3,Window.width*.1)
            restartButton.pos = Window.width*0.5-restartButton.width/2, Window.height*0.53
            restartButton.bind(on_release=restart_button)
            #we will want to bind the parent to listen for things from certain bubbles
 
        #*** It's important that the parent get the button so you can click on it
        #otherwise you can't click through the main game's canvas
            self.parent.add_widget(restartButton)
 
        #now draw the score widget
            self.showScore()
 
    def update(self,dt):
#This update function is the main update function for the game
#All of the game logic has its origin here
#events are setup here as well
 
        #update game objects
        #update ship
        self.ship.update()
        #update asteroids
        #randomly add an asteroid
        tmpCount = randint(1,1800)
        if tmpCount > self.minProb:
            self.addAsteroid()
            if self.minProb > 1300:
                self.minProb = 1300
            self.minProb = self.minProb -1
 
        for k in self.asteroidList:
            #check for collision with ship
            if k.collide_widget(self.ship):
        #game over routine
                self.gameOver()
                Clock.unschedule(self.update)
                #add reset button
                self.ship.explode()
                k.update()
            #check to see if asteroid is off of screen
            if k.x <  -100:
            #since it's off the screen, remove the asteroid
 
                self.remove_widget(k)
                self.asteroidScore = self.asteroidScore + 1
 
            #remove asteroids off screen
            tmpAsteroidList = self.asteroidList
            tmpAsteroidList[:] = [x for x in tmpAsteroidList if ((x.x > - 100))]
            self.asteroidList = tmpAsteroidList
 
class ClientApp(App):
 
    #this is the first thing made
    def build(self):
        #this is where the root widget goes
        #should be a canvas
        self.parent = Widget() #
 
        self.app = GUI()
        #Start the game clock (runs update function once every (1/60) seconds
        #Clock.schedule_interval(app.update, 1.0/60.0)
        #add the start menu
        self.sm = Start_Screen()
        self.parent.add_widget(self.sm)
        self.parent.add_widget(self.app) #use this hierarchy to make it easy to deal w/buttons

        #self.sm2 = TopMenu()
        #self.sm2.buildUp()
        #self.parent.add_widget(self.sm2)

        return self.parent
 
if __name__ == '__main__' :
    ClientApp().run()