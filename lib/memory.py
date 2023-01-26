from array import array

MEMORY_SIZE = 4096

class Memory:
    def __init__(self) -> None:
        self.memory = array('Q', [0] * MEMORY_SIZE)

    def read(self, address: int) -> int:
        return self.memory[address]

    def write(self, address: int, byte: int) -> None:
        self.memory[address] = byte