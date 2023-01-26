class Instruction:
    def __init__(self, instruction: int):
        self.type = instruction >> 12
        self.x = (instruction >> 8) & 0xf
        self.y = (instruction >> 4) & 0xf
        self.n = instruction & 0xf
        self.nn = instruction & 0xff
        self.nnn = instruction & 0xfff