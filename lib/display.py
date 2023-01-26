from array import array

WIDTH = 64
HEIGHT = 32

class Display:
    def __init__(self) -> None:
        self.display = [[False] * WIDTH for i in range(HEIGHT)]

    def on(self, x: int, y: int) -> None:
        self.display[y][x] = True

    def off(self, x: int, y: int) -> None:
        self.display[y][x] = False

    def clear(self) -> None:
        self.display = [[False] * WIDTH for i in range(HEIGHT)]

    def pixel(self, x: int, y: int) -> bool:
        return self.display[y][x]
    
    def flip(self, x: int, y: int) -> None:
        if self.pixel(x, y):
            self.off(x, y)
        else:
            self.on(x, y)