from lib.display import WIDTH, HEIGHT
from lib.keypad import KEYPAD
from lib.emulator import Emulator

import pygame

# Each pixel in CHIP-8 will be an 8x8 pixel on your screen
SCALE = 8

def main():
    file_name = input("File Name: ")
    file = open(f'roms/{file_name}', 'rb')

    pygame.init()
    screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    emulator = Emulator()
    emulator.read_file(file)
    pygame.display.set_caption('CHIP-8 Intepreter')
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key not in KEYPAD:
                    continue
                emulator.key_pressed = KEYPAD[key]
        
        if emulator.changed:
            emulator.update_screen(screen)

        emulator.run()      

if __name__ == "__main__":
    main()