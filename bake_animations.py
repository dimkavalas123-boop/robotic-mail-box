from program_controler import Controller,turn_path_to_img
from text_animations import TextManager
from animation_manager import Parallelogram,AnimationManager
import pygame
import os
import random

  
FPS = 15 

pygame.init()

dummy_window = pygame.Surface((320, 240), pygame.SRCALPHA)
pygame.display.set_mode((1, 1), pygame.HIDDEN)

c = Controller(dummy_window)
calendars = c.calendar.menu_calendar
options = c.calendar.main_menu_options

for indx,op in enumerate(options):

    if op == "EXIT":continue

    sample_calendar = calendars[op]

    photo_managers = sample_calendar.image_manager_pygame_photos

    for indx2,ph_mng in enumerate(photo_managers):
        main_folder_name = f"BakedAnimations/ImagesMove/{indx2}_{op}_calendar"

        for i in range(1):

            print(f"{indx}/{len(options)} - {indx2}/{len(photo_managers)} - {i}/3")

            max_deg = random.choice([-4,4])

            ph_mng.start_shuffle_animation(0.25,max_deg)

            folder_name = f"{main_folder_name}_{i+1}"

            try:
                os.mkdir(folder_name)
            except:
                pass

            frame_count = 0
            
            while ph_mng.animation_on :
                dummy_window.fill((0,0,0,0))
                ph_mng.update()

                filename = f"{folder_name}/frame_{frame_count:03d}.png"
                pygame.image.save(dummy_window, filename)

                frame_count += 1

