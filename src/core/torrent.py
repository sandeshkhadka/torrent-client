from hashlib import sha1

from .bencode import Decoder, Encoder


class Torrent:
    _meta: dict[bytes, bytes]
    _info_hash: bytes
    _info: dict[bytes,bytes]

    def __init__(self,file_path:str) -> None:
        self._file = file_path

        with open(self._file, 'rb') as file:
            decoded = Decoder(file.read()).decode()
            if not isinstance(decoded, dict):
                # print("Invalid torrent file strucutre")
                exit()
            self._meta = decoded
            # for key in self._meta.keys():
                # print(key.decode("utf-8"))
        info = self._meta[b'info']

        encoded_info = Encoder.encode(info)
        self._info_hash = sha1(encoded_info).digest()
        # print(f"Info Hash: {self._info_hash.hex()}")
        
        if not isinstance(info, dict):
            print("Info not found")
            exit()

        self._info = info

    @property
    def announce(self):
        announce = self._meta.get(b'announce',b'')
        if announce == b'':
            print("Announce not found")
            exit()
        return announce
    
    @property
    def announce_list(self):
        return self._meta[b'announce-list']
 
    @property
    def info(self):
        return self._meta[b'info']

    @property
    def creation_date(self):
        return self._meta[b'creation date']

    @property
    def comment(self):
        return self._meta[b'comment']

    @property
    def info_hash(self):
        return self._info_hash

    @property
    def encoding(self):
        return self._meta[b'encoding']

    @property 
    def total_size(self)-> int:
        if b'length' not in self._info.keys():
            print("Multi file not supported yet")

        return int(self._info[b'length'].decode("utf-8"))
        
    @property
    def created_by(self):
        return self._meta[b'created by']


