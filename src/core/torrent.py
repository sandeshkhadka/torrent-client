from hashlib import sha1

from .bencode import Decoder, Encoder


class Torrent:
    _meta: dict
    _info_hash: bytes
    _info: dict[bytes,bytes]

    def __init__(self,file_path:str) -> None:
        self._file = file_path

        with open(self._file, 'rb') as file:
            decoded = Decoder(file.read()).decode()
            if not isinstance(decoded, dict):
                print("Invalid torrent file strucutre")
                exit()
            self._meta = decoded
        info = self._meta[b'info']

        encoded_info = Encoder.encode(info)
        self._info_hash = sha1(encoded_info).digest()
        
        if not isinstance(info, dict):
            print("Info not found")
            exit()

        self._info = info

    @property
    def announce(self):
        return self._meta[b'announce']
    
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
    def total_size(self):
        if b'length' not in self._info.keys():
            print("Multi file not supported yet")

        return self._info[b'length']
        
    @property
    def created_by(self):
        return self._meta[b'created by']


