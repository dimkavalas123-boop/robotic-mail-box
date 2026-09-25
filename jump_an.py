import pygame


class JumpAnimation:
    def __init__(self,fps,window,screen_width,screen_height,x_pos,y_pos,x_vel,y_vel,rot_vel,text_surface,g=500,deg=0,time=1,font=None,opacity_change=0.5,color=[255,0,0]):
        self.fps = fps

        self.window = window

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.start_x = x_pos
        self.start_y = y_pos

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.start_vel_y = y_vel
        self.start_vel_x = x_vel
        self.start_rot_vel = rot_vel

        self.grav = g

        self.all_time = time
        self.all_frames = time*fps
        self.frame_now = -1
        self.time_now = None

        self.start_deg = deg
        self.deg = deg

        self.text_surface = text_surface

        self.opacity_change = opacity_change


    def update_pos_with_current_time(self):
        
        self.x_pos = self.time_now*self.start_vel_x + self.start_x
        self.y_pos = self.start_y + self.start_vel_y*self.time_now + 0.5*self.grav*(self.time_now**2)


    def update_rotation_with_current_time(self):

        self.deg = self.start_deg + self.start_rot_vel*self.time_now


    def give_moved_text(self):

        rotated_surface = pygame.transform.rotate(self.text_surface,self.deg)

        rotated_rect = rotated_surface.get_rect(center=(self.x_pos,self.y_pos))

        return rotated_surface,rotated_rect


    def update_frame(self):

        self.frame_now += 1
        self.time_now = self.frame_now/self.fps
        if self.frame_now >= self.all_frames:
            self.text_surface.set_alpha(255 )
            return

        
        self.update_pos_with_current_time()
        self.update_rotation_with_current_time()

        rotated_surface,rotated_rect = self.give_moved_text()

        if self.time_now >= self.all_time-self.opacity_change:
            elapsed_time = self.time_now- (self.all_time - self.opacity_change)
            ratio = elapsed_time/self.opacity_change
            self.text_surface.set_alpha(255*(1-ratio) )

        self.window.blit(rotated_surface,rotated_rect)





