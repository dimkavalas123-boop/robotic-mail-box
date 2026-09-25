from jump_an import JumpAnimation
import random
import math
import pygame

class ExplosionAnimation:
    def __init__(self,window,screen_width,screen_height,x_center,y_center,perigram,fps,text_surface,is_text=False,text=None,color=None,num = 5,max_time=1.3):

        self.window = window
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.x_center = x_center
        self.y_center = y_center

        self.perigram = perigram

        self.fps = fps

        self.text_surface = text_surface

        self.is_text = is_text
        if self.is_text:
            self.font = pygame.font.SysFont("Test.ttf",30)
            self.color = color
            self.text = text

        self.set_up_expl(num)

        self.frame_now = -1

        self.play = True
        self.max_time = max_time


    def set_up_expl(self,num):

        explosions = []

        for _ in range(num):

            noises = [random.randint(-1,1)*5*random.random() for _ in range(3)]
            noise_x,noise_y,noise_rot = noises[0],noises[1],noises[2]

            velocity = random.randint(150,350)
            rot_velocity = random.randint(50,200)

            random_start_deg = random.randint(-20,20)

            sample_x,sample_y = self.perigram.give_random_pos()

            Dx,Dy = (sample_x-self.x_center),(sample_y-self.y_center)

            distance = math.sqrt(Dx**2 + Dy**2)

            x_vel = (Dx/distance)*velocity
            y_vel = velocity*(Dy/distance)

            x_vel += noise_x
            y_vel += noise_y
            rot_velocity += noise_rot

            if self.is_text:
                noises = [random.randint(-1,1)*70*random.random() for _ in range(3)]
                new_color = [ min(max(self.color[i]+noises[i],0),255) for i in range(3)]
                self.text_surface = self.font.render(self.text,True,new_color)

            sample_explosion = JumpAnimation(self.fps,self.window,self.screen_width,self.screen_height,sample_x,sample_y,x_vel,y_vel,rot_velocity,self.text_surface,deg= random_start_deg)

            explosions.append(sample_explosion)

        self.explosions = explosions

    def update_frame(self):

        for exp in self.explosions:
            exp.update_frame()

        self.frame_now += 1
        if self.frame_now/self.fps >= self.max_time:
            self.play = False


