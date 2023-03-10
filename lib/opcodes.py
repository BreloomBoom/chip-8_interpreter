class Codes:
    CLEAR_SCREEN = 0xE0
    POP_PC = 0xEE

    REMOVAL = 0
    SET_PC_TO_NNN = 1
    PUSH_PC_AND_SET = 2

    VX_EQUALS_NN = 3
    VX_NOT_EQUALS_NN = 4
    VX_EQUALS_VY = 5
    VX_NOT_EQUALS_VY = 9

    SET_VX_TO_NN = 6
    ADD_NN_TO_VX = 7

    VX_VY_ARITHMETIC = 8
    SET_VX_TO_VY = 0
    VX_OR_XY = 1
    VX_AND_VY = 2
    VX_XOR_VY = 3
    VX_PLUS_VY = 4
    VX_MINUS_VY = 5
    VY_MINUS_VX = 7
    LEFT_SHIFT = 0xE
    RIGHT_SHIFT = 6

    SET_INDEX_TO_NNN = 0xA
    SET_PC_TO_NNN_PLUS_V0 = 0xB
    RAND_INT = 0xC
    DRAW = 0xD

    READ_KEY = 0xE
    KEY_PRESSED = 0x9E
    KEY_NOT_PRESSED = 0xA1

    OTHER = 0xF
    SET_X_TO_DELAY = 0x7
    SET_DELAY_TO_X = 0x15
    SET_SOUND_TO_X = 0x18
    ADD_X_TO_INDEX = 0x1E
    BLOCK_KEY_READ = 0xA
    SET_INDEX_FONT = 0x29
    CONVERT_BINARY = 0x33
    WRITE_MEMORY = 0x55
    READ_MEMORY = 0x65