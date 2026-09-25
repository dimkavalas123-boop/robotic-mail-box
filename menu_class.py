from text_animations import TextManager
import math
import pygame


class AdvancedMenuGeneral:
    def __init__(self,menu_options,window,screen_width,screen_height,horizontal = False,font=25,font_style=None,fps=12,max_items=4,baked=True):

        self.max_items = max_items
        self.menu_options = []
        self.menus = []
        self.menu_choice = 0

        self.window = window
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.horizontal = horizontal
        self.font = font
        self.font_style = font_style
        self.fps = fps
        self.baked = baked

        self.change_adv_menu_options(menu_options)

        self.image_pygame_photos = None
        self.image_show_list = [False for _ in range(len(self.menus))]

    def fix_menu_position(self,positions):
        for i,menu_positions in enumerate(positions):
            if menu_positions != None:
                self.menus[i].fix_position(menu_positions)         

    def add_photos(self,image_manager_pygame_photos):

        self.image_manager_pygame_photos = image_manager_pygame_photos

        for indx,img in enumerate(image_manager_pygame_photos):

            if img != None:
                self.image_show_list[indx] = True


    def get_up(self):
        if len(self.menus) == 1:
            self.menu_now.get_up()
            return

        all_items = self.max_items*(self.menu_choice) 
        all_items += self.menu_now.choice

        if all_items + 1 == len(self.menu_options):
            self.menu_choice = 0
            self.menu_now = self.menus[self.menu_choice]

        else:
            
            if math.floor((all_items + 1)/self.max_items) != math.floor(all_items /self.max_items):
                self.menu_now.choice = 0
                self.menu_choice += 1
                self.menu_now = self.menus[self.menu_choice]
            else:
                self.menu_now.get_up()


    def get_down(self):
        if len(self.menus) == 1:
            self.menu_now.get_down()
            return
        
        all_items = self.max_items*(self.menu_choice) 
        all_items += self.menu_now.choice
        
        if all_items - 1 == 0 or abs(all_items-1) == len(self.menu_options):
            if all_items -1 == 0:
                self.menu_choice = len(self.menu_options)-1
            elif abs(all_items-1) == len(self.menu_options):
                self.menu_choice = 0

            self.menu_now = self.menus[self.menu_choice]

        else:
            
            if math.floor((all_items - 1)/self.max_items) != math.floor(all_items /self.max_items):
                self.menu_now.choice = 0
                self.menu_choice -= 1
                self.menu_now = self.menus[self.menu_choice]
            else:
                self.menu_now.get_down()


    def change_adv_menu_options(self,new_options):
        old_num = len(self.menu_options)
        new_num = len(new_options)
        
        self.menu_options = new_options

        if old_num != new_num:

            self.menus = []
            self.menu_choice = 0

            for i in range(max(1,math.ceil(len(new_options)/self.max_items)) ):
                sample_menu = new_options[(i)*self.max_items:(i+1)*self.max_items]

                sample_menu = SimpleMenuGeneral(sample_menu,self.window,self.screen_width,self.screen_height,self.horizontal,self.font,self.font_style,self.fps,self.baked)
                self.menus.append(sample_menu)


        else:

            self.menu_choice = 0 

            for i in range(max(1,math.ceil(len(new_options)/self.max_items)) ):
                sample_menu = new_options[(i)*self.max_items:(i+1)*self.max_items]
                
                self.menus[i].menu_options = sample_menu

        self.menu_now = self.menus[self.menu_choice]
        self.menu_now.bool_update_set_up = True

    def update(self):
        self.menu_now.update()

        if self.image_show_list[self.menu_choice]:
            sample_img_manager = self.image_manager_pygame_photos[self.menu_choice]
            sample_img_manager.update()
    

class SimpleMenuGeneral:
    def __init__(self,menu_options,window,screen_width,screen_height,horizontal,font,font_style,fps,baked):
        self.window = window

        self.font = pygame.font.Font(font_style, font)
        self.menu_options = menu_options

        self.color_in = [255,255,0]
        self.color_out = [255,255,255]

        self.screen_width =screen_width
        self.screen_height = screen_height

        self.horizontal = horizontal

        self.choice = 0

        self.show_image = False
        self.image = None
        self.img_pos = None

        self.bool_update_set_up = True

        self.fps = fps

        self.text_managers = []

        self.fix_position_val = None 

        self.baked = baked

        self.update_set_up(True)

    def fix_position(self,position):
        self.fix_position_val = position


    def add_image(self,image_pygame,img_pos):

        self.show_image = True
        self.image = image_pygame
        self.img_pos = img_pos

        self.bool_update_set_up = True


    def get_up(self):
        self.choice += 1
        if self.choice  == len(self.menu_options):
            self.choice = 0

        if not self.baked:
            self.text_managers[self.choice].start_scale_animation(0.2,1.08)

        self.bool_update_set_up = True

    def get_down(self):
        self.choice -= 1
        if self.choice < 0:
            self.choice = len(self.menu_options)-1

        if not self.baked:
            self.text_managers[self.choice].start_scale_animation(0.2,1.08)

        self.bool_update_set_up = True


    def update(self):
        if self.bool_update_set_up:
            self.update_set_up()
            self.bool_update_set_up = False

        for text_manager in self.text_managers:
            text_manager.update()

        if self.show_image:
            self.window.blit(self.image,self.img_pos)

    def update_set_up(self,is_set_up=False):

        is_normal = bool(self.fix_position_val == None)

        for i, option in enumerate(self.menu_options):

            if i == self.choice:
                text_surface = self.font.render(option, True, self.color_in)
            else:
                text_surface = self.font.render(option, True, self.color_out)

            if is_normal:
                if not self.horizontal:
                    margin = self.screen_height//(1+len(self.menu_options))
                    text_rect = text_surface.get_rect(center=(self.screen_width // 2, margin + i*margin))
                else:
                    margin = self.screen_width//(1+len(self.menu_options))
                    text_rect = text_surface.get_rect(center=(  margin + i * margin,self.screen_height//2))
            else:
                pos = self.fix_position_val[i]
                text_rect = text_surface.get_rect(center=(pos[0],pos[1]))
            
            if is_set_up:
                
                sample_text_manager = TextManager(self.window,self.fps,text_surface,text_rect)
                self.text_managers.append(sample_text_manager)
            else:
                self.text_managers[i].text_surface = text_surface
                self.text_managers[i].text_rect = text_rect




        