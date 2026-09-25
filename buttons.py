import pygame
import RPi.GPIO as GPIO
import time

pygame.init()


K1_PRESSED = pygame.USEREVENT + 1
K2_PRESSED = pygame.USEREVENT + 2
K3_PRESSED = pygame.USEREVENT + 3

def k1_callback(channel):
    pygame.event.post(pygame.event.Event(K1_PRESSED))

def k2_callback(channel):
    pygame.event.post(pygame.event.Event(K2_PRESSED))

def k3_callback(channel):
    pygame.event.post(pygame.event.Event(K3_PRESSED))

def set_up_buttons():
    GPIO.setmode(GPIO.BOARD)
    buttons_pins = {12: "K1", 16: "K2", 18: "K3"}

    for pin, name in buttons_pins.items():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if name == "K1":
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=k1_callback, bouncetime=250)
        elif name == "K2":
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=k2_callback, bouncetime=250)
        elif name == "K3":
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=k3_callback, bouncetime=250)

