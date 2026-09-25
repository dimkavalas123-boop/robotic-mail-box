import random
import math
import pygame
import os
import pickle
from expl_an import ExplosionAnimation
from datetime import datetime
from loading_screen import show_loading_image

class AnimationManager:

    def __init__(self,window,screen_width,screen_height,fps,baked=False,g = None):

        self.g = g

        self.window = window

        self.screen_height = screen_height
        self.screen_width = screen_width

        self.fps = fps

        self.animations = []

        self.baked = baked

        if self.baked:
            self.set_up_baked()


    def play_explosion(self,x_center,y_center,perigram,num = 5,surface="text",text="<3",color=[255,0,0]):

        is_text = False
        if surface == "text":
            font = pygame.font.SysFont("Test.ttf",30)
            surface = font.render(text,True,color)
            is_text = True

        expl_an = ExplosionAnimation(self.window,self.screen_width,self.screen_height,x_center,y_center,perigram,self.fps,surface,is_text,text,color,num)

        self.animations.append(expl_an)


    def update_animations(self):

        for indx,an in enumerate(self.animations):

            an.update_frame()
            
            sample_play = an.play
            if not sample_play:
                self.animations.pop(indx)


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
    
    def set_up_baked(self):
            save_filepath = "short_baked_animations_cache.pkl"

            self.baked_an = {}


            animations = os.listdir("BakedAnimations")
            count = 0

            all_imgs = len(animations) + len(os.listdir("BakedAnimations/ImagesMove"))
            max_items = len(os.listdir("BakedAnimations")) -1 + len(os.listdir("BakedAnimations/ImagesMove"))

            for an in animations:
                count +=1
    
                print(f"{count}/{all_imgs} TO FTIUAXNO")
                
                if self.g.is_raspberry_pi and count%5 ==0:
                    show_loading_image(self.window,self.screen_width,self.screen_height,count-1,max_items)
                
                if an == "ImagesMove": continue
                sample_frames = load_baked_animation(f"BakedAnimations/{an}")
                self.baked_an[an] = sample_frames

            animations = os.listdir("BakedAnimations/ImagesMove")

            for an in animations:
                count +=1

                print(f"{count}/{all_imgs} TO GFTIAXNO")

                if self.g.is_raspberry_pi and count%5 == 0:
                    show_loading_image(self.window,self.screen_width,self.screen_height,count-1,max_items)

                sample_frames = load_baked_animation(f"BakedAnimations/ImagesMove/{an}")
                self.baked_an[an] = sample_frames

 
            
            if self.g.is_raspberry_pi:
                show_loading_image(self.window,self.screen_width,self.screen_height,0,0,"In a few seconds...")
            

                

    def play_baked_explosion(self,theme):
        r = random.randint(1,3)

        frames = self.baked_an[f"{theme}_explosion_{r}"]

        baked_animation = BakedAnimation(self.window,frames,self.screen_width,self.screen_height)

        self.animations.append(baked_animation)




def load_baked_animation(folder_path):
    frames = []

    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            path = os.path.join(folder_path, filename)

            frame_img = pygame.image.load(path).convert_alpha()
            frames.append(frame_img)
            
    return frames



class Circle:
    def __init__(self,x,y,radius):
        self.r = radius
        self.x_center = x
        self.y_center = y


    def give_random_pos(self):

        theta  = random.randint(0,360)
        rad_theta = (2*math.pi)*(theta/360)

        x_pos = self.r*math.sin(rad_theta) + self.x_center
        y_pos = self.r*math.cos(rad_theta) + self.y_center

        return x_pos,y_pos


class Parallelogram:
    def __init__(self,x,y,a,b):
        self.x_center = x
        self.y_center = y

        self.side1 = a
        self.side2 = b

    def give_random_pos(self):

        choice = random.randint(1,4)

        if choice == 1:
            x = self.x_center + self.side1//2
            y = self.y_center - self.side2//2 + self.side2*random.random()
        elif choice == 2:
            x = self.x_center - self.side1//2
            y = self.y_center - self.side2//2 + self.side2*random.random()
        elif choice == 3:
            x = self.x_center - self.side1//2 + self.side1*random.random()
            y = self.y_center + self.side2//2
        else:
            x = self.x_center - self.side1//2 + self.side1*random.random()
            y = self.y_center - self.side2//2

        return x,y


class BakedAnimation:
    def __init__(self,window,frames,screen_width,screen_height):

        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.window = window
        self.frames = frames

        self.all_frames = len(frames)
        self.frame_now = 0

        self.play = True

    def update_frame(self):

        if self.frame_now >= self.all_frames:
            self.play = False
            self.window.blit(self.current_image, self.rect)
            return

        self.current_image = self.frames[self.frame_now]
        
        self.rect = self.current_image.get_rect(center=(self.screen_width//2, self.screen_height//2))
        
        self.window.blit(self.current_image, self.rect)
        
        self.frame_now += 1