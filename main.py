import pygame
from program_controler import Controller
import threading
from datetime import datetime
from get_telegram import run_bot, msg_queue
import pickle

from global_var import Global

from ring_bell_func import ring_bell_now

screen_width,screen_height = 320,240
window = pygame.display.set_mode((screen_width,screen_height))
fps = 15

pygame.init()

K1_PRESSED = pygame.USEREVENT + 1
K2_PRESSED = pygame.USEREVENT + 2
K3_PRESSED = pygame.USEREVENT + 3

NEW_TELEGRAM_MSG = pygame.USEREVENT + 67



def main():
    t0 = datetime.now()
    baked = True

    g = Global()
    print(g.is_raspberry_pi)
    if g.is_raspberry_pi:
        fb_file = open("/dev/fb1", "wb")

        from buttons import set_up_buttons
        from update_screen import update_tft

        baked = True

        set_up_buttons()


    run = True
    clock = pygame.time.Clock()

    print("Kataskevazo controller")
    main_controller = Controller(window,fps=fps,baked=baked,g=g)
    print("Kataskevastike")

    print("Arxizo to threading")
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    print("Arxise telebot")

    print("Arxizo na dixno")
    t2 = datetime.now()

    print(f"To ekana se {t2-t0}")
    
    while run:
        clock.tick(fps)

        window.fill([0,0,0])

        while not msg_queue.empty():
            msg = msg_queue.get_nowait()
            if msg == "NEW_MSG":
                print("New msg received!")
                main_controller.change_notifications()


                if g.is_raspberry_pi and g.ring_bell:
                    ring_bell_now(13, g.ring_num)
                    ring_bell_now(12, 1, 1)


        for event in pygame.event.get():
            
            # if event.type == NEW_TELEGRAM_MSG:
            #     print("New ms")
            #     main_controller.change_notifications()
            #     if g.is_raspberry_pi and g.ring_bell:
            #         ring_bell_now(13,g.ring_num)
            #         ring_bell_now(12,1,1)

            if not g.is_raspberry_pi:
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        main_controller.get_down()
                    elif event.key == pygame.K_DOWN:
                        main_controller.get_up()
                    elif event.key == pygame.K_SPACE:
                        main_controller.check()

                
            else:
                if event.type == K1_PRESSED:
                    print("K1")
                    main_controller.get_down()
                elif event.type == K2_PRESSED:
                    main_controller.get_up()
                    print("K2")
                elif event.type == K3_PRESSED:
                    print("K3")
                    main_controller.check()

        main_controller.update()

        if g.is_raspberry_pi:
            update_tft(window, fb_file)
        else:
            pygame.display.update()

main() 