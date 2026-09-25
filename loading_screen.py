import pygame


def show_loading_image(window,screen_width,screen_height,n,max,text=None):
    
    from update_screen import update_tft

    fb_file = open("/dev/fb1", "wb")

    window.fill([0,0,0])
    font = pygame.font.Font("Test.ttf",18)
    if text == None:
        text = f"{round(100*(n/max),1)} % has been completed"

    text_pygame = font.render(text, True,[255,255,255])

    textRect = text_pygame.get_rect()

    textRect.center = (screen_width // 2, screen_height // 2)

    window.blit(text_pygame,textRect)

    update_tft(window, fb_file)
