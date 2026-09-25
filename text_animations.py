import math
import pygame
import random
from animation_manager import BakedAnimation

class TextManager:
    def __init__(self,window,fps,text_surface,text_rect):

        self.window = window

        self.fps = fps

        self.text_surface = text_surface
        self.text_rect = text_rect

        self.animation_on = False
        self.animation = None

        self.id = random.randint(1,100)

        self.width = self.text_surface.get_width()
        self.height = self.text_surface.get_height()

    def give_width(self):
        return self.width

    def give_height(self):
        return self.height

    def give_surface(self):
        return self.text_surface

    def give_rect(self):
        return self.text_rect

    def give_x(self):
        return self.text_rect.centerx
    
    def give_y(self):
        return self.text_rect.centery

    def start_shuffle_animation(self,period,max_angle,endless=False,start_deg=0):
        new_animation_shuffle = TextShuffleAnimation(self.window,self.fps,self,period,max_angle,endless,start_deg)

        self.animation = new_animation_shuffle

        self.animation_on = True

    def start_baked_animation(self,frames,screen_width,screen_height):

        new_baked = BakedAnimation(self.window,frames,screen_width,screen_height)

        self.animation = new_baked

        self.animation_on = True

    def start_scale_animation(self,time,max_scale):

        new_animation_scale = TextScaleAnimation(self.window,self.fps,self,max_scale,time)
        
        self.animation = new_animation_scale
        
        self.animation_on = True

    def update(self):


        if self.animation_on:
            self.animation.update_frame()
            if not self.animation.play:
                self.animation = None
                self.animation_on = False
        else:
            self.window.blit(self.text_surface,self.text_rect)

    #Ftiaxno apo surface se bytes kai to antistrofo
    def surface_to_data(self,surface):

        return {
            "pixels": pygame.image.tostring(surface, "RGBA"),
            "size": surface.get_size(),
            "mode": "RGBA"
        }

    def data_to_surface(self,data):

        return pygame.image.fromstring(
            data["pixels"], 
            data["size"], 
            data["mode"]
        ).convert_alpha()
    #-------------------------------------------

    #Kodikas gia na mpori na gini antigrafi se pkl
    def __getstate__(self):
        state = self.__dict__.copy()
        
        if "text_surface" in state:
            state["text_surface"] = self.surface_to_data(state["text_surface"])
            
        if "window" in state:
            del state["window"] 
            
        return state

    def __setstate__(self, state):

        if "text_surface" in state:
            state["text_surface"] = self.data_to_surface(state["text_surface"])
            
        self.__dict__.update(state)

    #--------------------------------------



class TextScaleAnimation:
    def __init__(self,window,fps,text_manager,max_scale,time):
        self.endless = False

        self.window = window
        self.fps = fps

        self.text_manager = text_manager

        self.max_scale = max_scale
        self.max_time = time

        self.play = True

        self.time_now = 0
        self.frame_now = 0
        self.all_frames = self.max_time*self.fps

        self.scale = 1

    def update_scale(self):
        
        b = (4*(self.max_scale-1))/self.max_time
        a = -b/self.max_time
        c = 1

        self.scale = a*(self.time_now**2) + b*self.time_now + c

    def move_text(self):
        x_pos, y_pos = self.text_manager.give_x(), self.text_manager.give_y()

        rotated_surface = pygame.transform.rotozoom(self.text_manager.text_surface, 0, self.scale)
        
        rotated_rect = rotated_surface.get_rect(center=(x_pos, y_pos))

        return rotated_surface, rotated_rect

    def update_frame(self):

        self.update_scale()

        self.frame_now += 1
        self.time_now = self.frame_now/self.fps 

        
        if self.frame_now >= self.all_frames:
            self.play = False

        rotated_surface, rotated_rect = self.move_text()
        
        self.window.blit(rotated_surface, rotated_rect)

        

    
class TextShuffleAnimation: #Xronos -1 gia endless

    def __init__(self,window,fps,text_manager,period,max_angle,endless = False,start_deg=0):

        self.endless = endless

        self.window = window
        self.fps = fps

        self.text_manager = text_manager

        self.period = period
        self.max_angle = max_angle

        self.deg = 0

        self.rot_vel = (2*math.pi)/(self.period)

        self.time_now = 0
        self.frame_now = 0
        self.all_frames = self.period*self.fps

        self.play = True

        self.start_f0 = math.asin(start_deg)


    def update_angle(self):

        self.deg =  self.max_angle*math.sin(self.rot_vel*self.time_now + self.start_f0)


    def update_frame(self):
            self.update_angle()

            self.frame_now += 1
            self.time_now = self.frame_now / self.fps
            if (self.frame_now >= self.all_frames) and (not self.endless):
                self.play = False

            rotated_surface, rotated_rect = self.move_text()

            self.window.blit(rotated_surface, rotated_rect)

    def move_text(self):
        x_pos, y_pos = self.text_manager.give_x(), self.text_manager.give_y()

        rotated_surface = pygame.transform.rotozoom(self.text_manager.text_surface, self.deg, 1.0)
        
        rotated_rect = rotated_surface.get_rect(center=(x_pos, y_pos))

        return rotated_surface, rotated_rect

        

    
