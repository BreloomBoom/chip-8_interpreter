from .memory import Memory
from .display import Display, WIDTH, HEIGHT
from .decode import Instruction
from .opcodes import Codes
from .font import FONT

import pygame
from random import randint

BYTE_SIZE = 8
INCREMENT = 2
UINT8_LIMIT = 256
SCALE = 8
UINT12_LIMIT = 4096
NOTHING_PRESSED = -1
DECREMENT = 0.25

class Emulator:
    def __init__(self) -> None:
        self.memory = Memory()
        self.display = Display()
        self.stack = []
        self.pc = 0x200
        self.index = 0
        self.delay_timer = 0
        self.sound_timer = 0
        self.registers = [0] * 16
        self.changed = False
        self.key_pressed = NOTHING_PRESSED

    def read_file(self, file) -> None:
        for i in range(len(FONT)):
            self.memory.write(i, FONT[i])

        ba = bytearray(file.read())
        for i in range(len(ba)):
            self.memory.write(0x200 + i, ba[i])

    def run(self) -> None:
        self.execute(self.fetch())
        self.key_pressed = NOTHING_PRESSED
        self.delay_timer -= DECREMENT
        self.sound_timer -= DECREMENT

    def fetch(self) -> Instruction:
        instruction = self.memory.read(self.pc) * UINT8_LIMIT + self.memory.read(self.pc + 1)
        self.pc += INCREMENT

        return Instruction(instruction)
    
    def execute(self, i: Instruction) -> None:
        match i.type:
            case Codes.REMOVAL:
                if i.nn == Codes.CLEAR_SCREEN:
                    self.display.clear()
                if i.nn == Codes.POP_PC:
                    self.pc = self.stack.pop()
            case Codes.SET_PC_TO_NNN:
                self.pc = i.nnn
            case Codes.PUSH_PC_AND_SET:
                self.stack.append(self.pc)
                self.pc = i.nnn
            case Codes.VX_EQUALS_NN:
                self.pc += (self.registers[i.x] == i.nn) * INCREMENT
            case Codes.VX_NOT_EQUALS_NN:
                self.pc += (self.registers[i.x] != i.nn) * INCREMENT
            case Codes.VX_EQUALS_VY:
                self.pc += (self.registers[i.x] == self.registers[i.y]) * INCREMENT
            case Codes.VX_NOT_EQUALS_VY:
                self.pc += (self.registers[i.x] != self.registers[i.y]) * INCREMENT
            case Codes.SET_VX_TO_NN:
                self.registers[i.x] = i.nn
            case Codes.ADD_NN_TO_VX:
                self.registers[i.x] = (self.registers[i.x] + i.nn) % UINT8_LIMIT
            case Codes.VX_VY_ARITHMETIC:
                match i.n:
                    case Codes.SET_VX_TO_VY:
                        self.registers[i.x] = self.registers[i.y]
                    case Codes.VX_OR_XY:
                        self.registers[i.x] = self.registers[i.x] | self.registers[i.y]
                    case Codes.VX_AND_VY:
                        self.registers[i.x] = self.registers[i.x] & self.registers[i.y]
                    case Codes.VX_XOR_VY:
                        self.registers[i.x] = self.registers[i.x] ^ self.registers[i.y]
                    case Codes.VX_PLUS_VY:
                        new_VX = self.registers[i.x] + self.registers[i.y]
                        self.registers[0xF] = new_VX >= UINT8_LIMIT
                        self.registers[i.x] = new_VX % UINT8_LIMIT
                    case Codes.VX_MINUS_VY:
                        new_VX = self.registers[i.x] - self.registers[i.y]
                        self.registers[0xF] = new_VX > 0
                        self.registers[i.x] = (new_VX + UINT8_LIMIT) % UINT8_LIMIT
                    case Codes.VY_MINUS_VX:
                        new_VX = self.registers[i.y] - self.registers[i.x]
                        self.registers[0xF] = new_VX > 0
                        self.registers[i.x] = (new_VX + UINT8_LIMIT) % UINT8_LIMIT
                    case Codes.RIGHT_SHIFT:
                        self.registers[0xF] = self.registers[i.x] % 2
                        self.registers[i.x] >>= 1
                    case Codes.LEFT_SHIFT:
                        self.registers[0xF] = self.registers[i.x] >> (BYTE_SIZE - 1)
                        self.registers[i.x] <<= 1
                        self.registers[i.x] = self.registers[i.x] % UINT8_LIMIT
            case Codes.SET_INDEX_TO_NNN:
                self.index = i.nnn
            case Codes.SET_PC_TO_NNN_PLUS_V0:
                self.pc = i.nnn + self.registers[0]
            case Codes.RAND_INT:
                self.registers[i.x] = randint(0, 256) & i.nn
            case Codes.DRAW:
                self.update_display(i.x, i.y, i.n)
            case Codes.READ_KEY:
                if i.nn == Codes.KEY_PRESSED:
                    if self.registers[i.x] == self.key_pressed:
                        self.pc += 2
                if i.nn == Codes.KEY_NOT_PRESSED:
                    if self.registers[i.x] != self.key_pressed:
                        self.pc += 2
            case Codes.OTHER:
                match i.nn:
                    case Codes.SET_X_TO_DELAY:
                        self.registers[i.x] = self.delay_timer
                    case Codes.SET_DELAY_TO_X:
                        self.delay_timer = self.registers[i.x]
                    case Codes.SET_SOUND_TO_X:
                        self.sound_timer = self.registers[i.x]
                    case Codes.ADD_X_TO_INDEX:
                        self.index  = (self.index + self.registers[i.x]) % UINT12_LIMIT
                    case Codes.BLOCK_KEY_READ:
                        if self.key_pressed == NOTHING_PRESSED:
                            self.pc -= 2
                        else:
                            self.registers[i.x] = self.key_pressed
                    case Codes.SET_INDEX_FONT:
                        self.index = self.registers[i.x] * 5
                    case Codes.CONVERT_BINARY:
                        self.memory.write(self.index + 2, self.registers[i.x] % 10)
                        self.memory.write(self.index + 1, (self.registers[i.x] // 10) % 10)
                        self.memory.write(self.index, (self.registers[i.x] // 100) % 10)
                    case Codes.WRITE_MEMORY:
                        for j in range(i.x + 1):
                            self.memory.write(self.index + j, self.registers[j])
                    case Codes.READ_MEMORY:
                        for j in range(i.x + 1):
                            self.registers[j] = self.memory.read(self.index + j)

    def update_display(self, x_index, y_index, n):
        y = self.registers[y_index] % HEIGHT
        self.registers[0xF] = 0

        for i in range(n):
            sprite_data = self.memory.read(self.index + i)
            x = self.registers[x_index] % WIDTH

            for j in range(BYTE_SIZE):
                isBitSet = (sprite_data >> (BYTE_SIZE - j - 1)) & 1
                if isBitSet:
                    if self.display.pixel(x, y):
                        self.registers[0xF] = self.display.pixel(x, y)
                    self.display.flip(x, y)
                    self.changed = True
                
                if x == WIDTH - 1:
                    break
                x += 1
            
            y += 1
            if y == HEIGHT - 1:
                break

    def update_screen(self, screen: pygame.Surface):
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if self.display.pixel(i, j):
                    pygame.draw.rect(screen, (255,255,255), pygame.Rect(i * SCALE, j * SCALE, SCALE, SCALE))
                else:
                    pygame.draw.rect(screen, (0,0,0), pygame.Rect(i * SCALE, j * SCALE, SCALE, SCALE))
        
        pygame.display.flip()
        self.changed = False