#!/usr/bin/python
# Filename: Touch_Training_menus_classes.py




class Twoimages(Paradigm_Base):
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
  
    #what happen if a button is pressed
    def do_on_release(self):
        print self.buttonText
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
        



def TwoImages():
	print 'strifun'
	self.current_paradigm = Paradigm_Two_choice_images()
    self.current_paradigm.buildUp()
    self.parent.add_widget(self.current_paradigm)

version = '0.1'

# End of Touch_Training_menus_classes.py
			