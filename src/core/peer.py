import socket
from hashlib import sha1


class PeerConnection:
    def __init__(self, ip, port, info_hash, peer_id):
        self.ip = ip
        self.port = port
        self.info_hash: bytes = info_hash
        self.peer_id: bytes = peer_id
        self.socket = None

    def connect(self):
        self.socket = socket.create_connection((self.ip, self.port), timeout=5)
        self._handshake()

    def _handshake(self):
        pstr = b'BitTorrent protocol'
        msg = bytes([len(pstr)]) + pstr + bytes(8) + self.info_hash + self.peer_id
        if self.socket is None:
            raise Exception("Socket not connected")
        self.socket.sendall(msg)
        response = self.socket.recv(68)

        if len(response) < 68 or response[1:20] != pstr:
            raise Exception('Invalid handshake response')

        print(f"Handshake complete with {self.ip}:{self.port}")

