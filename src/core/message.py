KEEP_ALIVE = -1
CHOKE = 0
UNCHOKE = 1
INTERESTED = 2
NOT_INTERESTED = 3
HAVE = 4
BITFIELD = 5
REQUEST = 6
PIECE = 7
CANCEL = 8

def build_interested():
    return b'\x00\x00\x00\x01' + bytes([INTERESTED])

