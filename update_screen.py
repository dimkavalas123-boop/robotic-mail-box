import numpy as np
import pygame

try:
    fb_file = open("/dev/fb1", "wb")
except PermissionError:
    print("sfalma")
    exit(1)

def update_tft(surface, fb_file):

    width, height = surface.get_size()

    raw_bytes = pygame.image.tostring(surface, "RGB", False)

    rgb = np.frombuffer(raw_bytes, dtype=np.uint8).reshape((height, width, 3))
    
    r = (rgb[:, :, 0] >> 3).astype(np.uint16) << 11
    g = (rgb[:, :, 1] >> 2).astype(np.uint16) << 5
    b = (rgb[:, :, 2] >> 3).astype(np.uint16)
    rgb565 = r | g | b  

    fb_file.seek(0)
    fb_file.write(rgb565.tobytes())
