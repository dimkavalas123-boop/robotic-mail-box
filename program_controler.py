import pygame
import pickle
from datetime import datetime
import random
import json
import os
from menu_class import AdvancedMenuGeneral,SimpleMenuGeneral
from animation_manager import AnimationManager,Circle,Parallelogram
from text_animations import TextManager
import subprocess
from time import sleep
import shutil

from loading_screen import show_loading_image

class Controller:
    def __init__(self,window,font_style ="Test.ttf",screen_width=320,screen_height = 240,fps=12,font=18,baked=False,g=None):

        self.window = window
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.g = g

        print("Kano to animation manager")
        self.animation_manager = AnimationManager(window,screen_width,screen_height,fps,baked,self.g)
        print("Egine animation")

        print("ftiaxno to main menu")
        self.main_menu = MainMenu(window,screen_width,screen_height,self.animation_manager,font,font_style,fps,baked,self.g)
        print("egine to main menu")

        print("ftiaxno ta notification")
        self.notifications = NotificationsMenu(window,screen_width,screen_height,font,font_style,fps,baked)
        print("eginan notification")

        print("ftiaxno to calendar")
        self.calendar = CalendarMenu(window,screen_width,screen_height,self.animation_manager,font,font_style,fps,baked)
        print("egine to calendar")

        print("ftiaxno ta settings")
        self.settings = Settings(window,screen_width,screen_height,font,font_style,fps,baked)
        print("eginan ta settings")

        self.choices = ["Menu","Notifications","Settings","Calendar"]


        self.now = self.choices[0]


    def update(self):
        #self.msg_menu.update()
        t1 = datetime.now()

        if self.now == "Menu":
            self.main_menu.update()
        elif self.now == "Notifications":
            self.notifications.update()
        elif self.now == "Calendar":
            self.calendar.update()
        elif self.now == "Settings":
            self.settings.update()

        t2 = datetime.now()
        self.animation_manager.update_animations()

    def get_down(self):
        if self.now == "Menu":
            self.main_menu.get_down()
        elif self.now == "Calendar":
            self.calendar.get_down()
        elif self.now == "Settings":
            self.settings.get_down()

    def get_up(self):
        if self.now == "Menu":
            self.main_menu.get_up()
        elif self.now == "Calendar":
            self.calendar.get_up()
        elif self.now == "Settings":
            self.settings.get_up()


    def check(self):
        if self.now == "Menu":
            result = self.main_menu.check()
            
            if "NO NOTIFICATIONS" in result:
                print("tpt vlaka")
                pass
            elif "NOTIFICATIONS:" in  result:
                self.now = "Notifications"
                self.notifications.start()
            elif "CALENDAR" in result:
                self.now = "Calendar"
            elif "SETTINGS" in result:
                self.now = "Settings"

        elif self.now == "Notifications":
            result = self.notifications.check()
            if result:
                print("teliosa")
                self.now = "Menu"
                self.main_menu.change_notification_num(False)

        elif self.now == "Calendar":

            result = self.calendar.check()
            if result == "EXIT":
                self.now = "Menu"
                self.main_menu.change_notification_num(False)

        elif self.now == "Settings":

            result = self.settings.check()

            if result == "RingBell":

                self.settings.menu_options_dict[result] = not self.settings.menu_options_dict[result]

                self.g.ring_bell = self.settings.menu_options_dict[result]

            elif result == "Rings":

                self.settings.menu_options_dict[result] += 1
                if self.settings.menu_options_dict[result] > 7:
                    self.settings.menu_options_dict[result] = 2

                self.g.ring_num = self.settings.menu_options_dict[result]

            elif result == "Exit":

                self.now = "Menu"
                self.main_menu.change_notification_num(False)

            elif result == "CloseRobot":
    
                show_loading_image(self.window,self.screen_width,self.screen_height,0,0,"Unplug when screen white")

                sleep(0.7)
                
                subprocess.run(["sudo", "shutdown", "-h", "now"])

                sleep(15)

    def change_notifications(self):
        if self.now == "Menu":
            self.main_menu.change_notification_num()
            



class MainMenu:

    def __init__(self,window,screen_width,screen_height,animation_manager,font,font_style,fps,baked,g):

        self.g = g 

        self.baked = baked

        self.animation_manager = animation_manager

        self.window = window

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.unread_msgs = 0
        self.menu_options = ["CALENDAR",f"NOTIFICATIONS: {self.unread_msgs}","SETTINGS"]

        self.menu_face = AdvancedMenuGeneral( self.menu_options,self.window,screen_width,screen_height,False,font,font_style,fps,baked=baked)

        self.change_interface = False

        heart_image,_,_ = turn_path_to_img("menuPhotos/heart.png",20)
        self.heart_image = heart_image

        self.change_notification_num(False)
            

    def change_notification_num(self,play_animation = True):

        #Play animation explosion (not the start)
    
        if play_animation:

            #Baked animations
            if self.baked:
                self.animation_manager.play_baked_explosion("notifications")
            
            #Manual animations
            else:
                text_manager = self.menu_face.menu_now.text_managers[1]

                max_deg = random.randint(-4,4)
                if max_deg == 0:
                    max_deg = 1
                text_manager.start_shuffle_animation(0.6,max_deg)           

                text_rect_given = text_manager.give_rect()

                width,height = text_rect_given.width,text_rect_given.height
                x,y = text_rect_given.centerx,text_rect_given.centery

                p = Parallelogram(x,y,1.5*width,2*height)
        
                self.animation_manager.play_explosion(x,y,p,5,self.heart_image)

            

        #Change number

        with open("texts/delivered.json","r") as file:
            content = json.load(file)

        file.close()
        self.unread_msgs = len(list(content))

        if self.unread_msgs == 0:
            self.menu_options[-2] = f"NO NOTIFICATIONS"
        else:
            self.menu_options[-2] = f"NOTIFICATIONS:{self.unread_msgs}"
        

        self.change_interface = True



        
    def get_up(self):
        self.menu_face.get_up()

    def get_down(self):
        self.menu_face.get_down()


    def update(self):
        if self.change_interface:
            self.menu_face.change_adv_menu_options(self.menu_options)
            self.animations_to_do = []
            self.change_interface = False

        self.menu_face.update()


    def check(self):

        choice_indx = self.menu_face.menu_now.choice

        return self.menu_options[choice_indx]



class NotificationsMenu:
    def __init__(self,window,screen_width,screen_height,font=25,font_style=None,fps=12,baked=True):

        self.window = window

        self.font = font
        self.font_style = font_style

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.scaler_image = 170

        self.fps = fps

        self.deg_now = 0

        self.baked = baked


    def start(self):
        self.msgs_delivered = self.read_all_delivered()

        self.choice = -1

        self.image_now = self.find_image_to_show()

    def read_all_delivered(self):
        
        with open("texts/delivered.json","r") as file:
            content = json.load(file)
        file.close()
        return content

    def update(self):
        self.image_now.update()

    def find_image_to_show(self,text_to_say="A NEW MESSAGE FROM LOVER <3"):

        if self.choice != -1 and (not self.baked):
            self.deg_now = self.image_now.menu_now.text_managers[0].animation.deg

        self.choice += 1
        sample_entry = self.msgs_delivered[self.choice]
        isText = sample_entry["isText"]
        time = sample_entry["Time"]

        if not isText:
            
            sample_options = [text_to_say,"","","","","","","",""]
            sample_menu = AdvancedMenuGeneral(sample_options,self.window,self.screen_width,self.screen_height,False,self.font,self.font_style,self.fps,baked=self.baked)
            sample_menu.max_items = len(sample_options)

            sample_menu.menu_now.color_in = [255,255,255]
            sample_menu.font *= 0.8

            photo_path = sample_entry["ImagePath"]
            
            img,new_width,new_height = turn_path_to_img(photo_path,self.scaler_image)

            left,top = self.screen_width//2-new_width//2,int(self.screen_height*0.27)

            img_rect = pygame.Rect(left,top,new_width,new_height)

            img_manager = TextManager(self.window,self.fps,img,img_rect)

            img_manager.start_scale_animation(0.2,1.2)

            sample_menu.add_photos([img_manager])


        else:
            
            content = self.msgs_delivered[self.choice]["Content"]

            msg = f'Msg: "{content}" '

            sample_options = [text_to_say,msg,"",""]

            sample_menu = AdvancedMenuGeneral(sample_options,self.window,self.screen_width,self.screen_height,False,self.font,self.font_style,self.fps,baked=self.baked)
            sample_menu.max_items = len(sample_options)
            
            sample_menu.menu_now.color_in = [255,255,255]

        if not self.baked:
            text_manager_title = sample_menu.menu_now.text_managers[0]
            text_manager_title.start_shuffle_animation(3,1,True,self.deg_now)

            text_manager_content = sample_menu.menu_now.text_managers[1]
            text_manager_content.start_scale_animation(0.2,1.4)
        
        return sample_menu

    def read_msgs(self):

        with open("texts/delivered.json","w") as f:
            json.dump([],f)
        f.close()

        folder_path = 'photos'

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:

                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Διαγραφή αρχείου
                
            except Exception as e:
                print(f' {file_path}: {e}')

    def check(self):
        if self.choice + 1 == len(self.msgs_delivered):
            print("LMAOOO")
            self.read_msgs()
            return True
        
        self.image_now = self.find_image_to_show()
        return False





class CalendarMenu:
    def __init__(self,window,screen_width,screen_height,animation_manager,font=25,font_style=None,fps=12,baked=False):

        self.baked = baked

        self.window = window

        self.font = font
        self.font_style = font_style

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.fps = fps

        self.main_menu_options = ["MYTILINH","KALAVRYTA","LT","OTHER","EXIT"]

        self.scaler_image = 170

        self.animation_manager = animation_manager
        print("Ftiaxno to menu tou calendar")
        self.create_menu()
        print("To eftiaksa")

        print("Ftiaxno ta idia ta calendars")
        self.menu_calendar = {}
        for theme in list(self.main_menu_options):

            if theme == "EXIT":continue

            print(f"Kano to {theme}")

            sample_calendar = self.create_calendar(f"{theme}_photos")

            self.menu_calendar[theme] = sample_calendar
        print("Ta eftiaksa")

        self.is_in_calendar = False

        self.calendar_now = None

        
    def create_menu(self):

        self.menu_face = AdvancedMenuGeneral( self.main_menu_options,self.window,self.screen_width,self.screen_height,False,self.font,self.font_style,self.fps,1,self.baked)
        header_position = [self.screen_width//2,int(self.screen_height*0.15)]

        self.menu_face.fix_menu_position([ [header_position] for _ in range(len(self.main_menu_options)) ])

        all_images_managers = []
        for theme in self.main_menu_options:
            ph = f"{theme}_photo.jpg"
            if theme == "EXIT":
                ph = f"{theme}_photo.png"

            img,new_width,new_height = turn_path_to_img(f"menuPhotos/{ph}",self.scaler_image)

            left,top = self.screen_width//2-new_width//2,int(self.screen_height*0.27)

            img_rect = pygame.Rect(left,top,new_width,new_height)

            img_manager = TextManager(self.window,self.fps,img,img_rect)
            all_images_managers.append(img_manager)

        self.menu_face.add_photos(all_images_managers)

        #Ftiaxo apo tora ta surfaces opou tha petagontai sto explosion
        self.explosions_photo_path = {"KALAVRYTA":"snowman.png",
                           "LT":"lt_logo.png",
                           "MYTILINH":"ouzo_plomariou.png",
                           "OTHER":"heart.png",
                           "EXIT":"sad.png"}

        self.explosions_scale = {"KALAVRYTA":50,
                                "LT":40,
                                "MYTILINH":40,
                                "OTHER":20,
                                "EXIT":40}

        self.explosion_images = {}
        for exp in list(self.explosions_photo_path):
            ph = self.explosions_photo_path[exp]
            sample_scale = self.explosions_scale[exp]
            sample_img,_,_ = turn_path_to_img(f"menuPhotos/{ph}",sample_scale)
            self.explosion_images[exp] = sample_img
        

    def create_calendar(self,folder):
        
        if not os.path.exists(f"PKLImages/{folder}.pkl"):
            print(f"Ftiaxno eikones {folder}")
            #Dimiourgia listas me ta photo managers tou sigkekrimenou folder
            all_img_paths = os.listdir(folder)

            photo_managers = []
            for ph in all_img_paths:
                sample_img,new_width,new_height = turn_path_to_img(f"{folder}/{ph}",self.scaler_image)

                left,top = self.screen_width//2-new_width//2,int(self.screen_height*0.27)
                
                sample_img_rect = pygame.Rect(left,top,new_width,new_height)

                sample_img_manager = TextManager(self.window,self.fps,sample_img,sample_img_rect)

                photo_managers.append(sample_img_manager)

            #Kano save se pkl oste na min ksanaxriasti

            with open(f"{folder}.pkl","wb") as file:
                pickle.dump(photo_managers,file)
            
        else:
            print(f"Xrisimopoio eikones pkl {folder}")
            #Kano load tin lista
            with open(f"PKLImages/{folder}.pkl", "rb") as file:
                photo_managers = pickle.load(file)

            #Ta text managers den exoun to window parameter
            for i in range(len(photo_managers)):
                photo_managers[i].window = self.window

        file.close()

        sample_option = "EXIT TO MAIN "
        real_options = []
        header_position = [self.screen_width//2,int(self.screen_height*0.15)]#
        all_positions = []
        for i in range(len(photo_managers)):
            all_positions.append([header_position])
            real_options.append(f"{sample_option} {i+1}/{len(photo_managers)} ")

        sample_calendar = AdvancedMenuGeneral(real_options,self.window,self.screen_width,self.screen_height,True,self.font,self.font_style,self.fps,1,self.baked)
        sample_calendar.fix_menu_position(all_positions)

        sample_calendar.add_photos(photo_managers)

        return sample_calendar


    def explosion_animation_change(self):
        choice = self.menu_face.menu_choice
        option_now = self.main_menu_options[choice]

        if not self.baked:
    
            img_manager_pygame = self.menu_face.image_manager_pygame_photos[choice]
            img_center = img_manager_pygame.give_x(),img_manager_pygame.give_y()

            width,height = img_manager_pygame.give_width(),img_manager_pygame.give_height()

            p = Parallelogram(img_center[0],img_center[1],1.2*width,1.2*height)
            n  = random.randint(2,5)

            surface_image = self.explosion_images[option_now]

            self.animation_manager.play_explosion(img_center[0],img_center[1],p,n,surface_image)

        else:

            theme = self.explosions_photo_path[option_now].split(".")[0]
            self.animation_manager.play_baked_explosion(theme)

    def move_header_text(self):

        text_manager = self.menu_face.menu_now.text_managers[0]

        max_deg = random.randint(-4,4)
        if max_deg == 0:
            max_deg = 1
        text_manager.start_shuffle_animation(0.3,max_deg)

    def move_photo_menu(self):
        
        choice = self.menu_face.menu_choice
        img_manager_pygame = self.menu_face.image_manager_pygame_photos[choice]

        max_deg = random.randint(-4,4)
        if max_deg == 0:
            max_deg = 1
        img_manager_pygame.start_shuffle_animation(0.3,max_deg)

    def move_photo_calendar(self):
        choice = self.calendar_now.menu_choice
        img_manager_pygame = self.calendar_now.image_manager_pygame_photos[choice]

        if not self.baked:
    
            max_deg = random.randint(-4,4)
            if max_deg == 0:
                max_deg = 1
            img_manager_pygame.start_shuffle_animation(0.3,max_deg)

        else:
            choice_op = self.menu_face.menu_choice
            option_now = self.main_menu_options[choice_op]

            if choice < 0:
                choice += len(self.calendar_now.menus)

            an_name = f"{choice}_{option_now}_calendar_1"
            frames = self.animation_manager.baked_an[an_name]

            img_manager_pygame.start_baked_animation(frames,self.screen_width,self.screen_height)


    def get_up(self):
        if not self.is_in_calendar:
            self.menu_face.get_up()
            self.explosion_animation_change()

            if not self.baked:
                self.move_header_text()
                self.move_photo_menu()

        else:
            self.calendar_now.get_down() #volevi na einai to down etsi
            self.move_photo_calendar()

    def get_down(self):
        if not self.is_in_calendar:
            self.menu_face.get_down()
            self.explosion_animation_change()
            
            if not self.baked:
                self.move_header_text()
                self.move_photo_menu()
        else:
            self.calendar_now.get_up() #volevi na einai to up etsi
            self.move_photo_calendar()

    def update(self):

        if not self.is_in_calendar:
            self.menu_face.update()
        else:
            self.calendar_now.update()

    def check(self):
        if not self.is_in_calendar:

            choice = self.menu_face.menu_choice
            option_now = self.main_menu_options[choice]

            if option_now == "EXIT":
                return option_now
            else:
                self.is_in_calendar = True
                self.calendar_now = self.menu_calendar[option_now]

        else:
            self.is_in_calendar = False
            self.menu_face.menu_choice = 0

def turn_path_to_img(photo_path,scaler_image):
    img = pygame.image.load(photo_path).convert_alpha()
    width,height = img.get_size()[0],img.get_size()[1]

    if width > height:
        ratio = (scaler_image/width)
        img = pygame.transform.scale(img, (scaler_image,int(height*ratio)))
        new_width,new_height = scaler_image,int(height*ratio)
    else:
        ratio = (scaler_image/height)
        img = pygame.transform.scale(img, (int(width*ratio),scaler_image))
        new_width,new_height = int(width*ratio),scaler_image

    return img,new_width,new_height


class Settings:
    def __init__(self,window,screen_width,screen_height,font=25,font_style = None,fps = 12,baked = False):

        self.baked = baked
        self.window = window

        self.font = font
        self.font_style = font_style

        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.fps = fps

        self.menu_options = ["Ring Bell: True","Rings: 2","Close Robot","Exit"]

        self.menu_options_dict = {"RingBell":True,"Rings":2}

        self.change_interface = True

        self.menu_face = AdvancedMenuGeneral( self.menu_options,self.window,screen_width,screen_height,False,font,font_style,fps,baked=baked)


    def get_up(self):
        self.menu_face.get_up()

    def get_down(self):
        self.menu_face.get_down()

    def update(self):
    
        if self.change_interface:
            for i in self.menu_options:
                print(i)
                if "Bell" in i:
                    self.menu_options[0] = f"Ring Bell: {str(self.menu_options_dict['RingBell'])}"
                elif "Rings" in i:
                    self.menu_options[1] = f"Rings: {self.menu_options_dict['Rings']}"
                
            

            self.menu_face.change_adv_menu_options(self.menu_options)
            self.change_interface = False

        self.menu_face.update()


    def check(self):

        choice_indx = self.menu_face.menu_now.choice

        self.change_interface = True

        choice = self.menu_options[choice_indx]

        print(self.change_interface,choice,"lMAOO")

        if "Bell" in choice:
            return "RingBell"
        elif "Rings" in choice:
            return "Rings"
        elif "Close" in choice:
            return "CloseRobot"
        
        return "Exit"