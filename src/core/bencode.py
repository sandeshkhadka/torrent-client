from enum import Enum


class TOKENS(Enum):
    INTEGER = b'i'
    LIST = b'l'
    DICT = b'd'
    END = b'e'
    SEPERATOR = b':'

class Decoder:

    def __init__(self, data: bytes) -> None:
        self._data = data
        self._index = 0

    def decode(self):
        token = self._get()
        if token == TOKENS.INTEGER.value:
            return self._decode_int()
        elif token == TOKENS.DICT.value:
            return self._decode_dict()
        elif token == TOKENS.LIST.value:
            return self._decode_list()
        elif token.isdigit():
            self._unget()
            return self._decode_string()

    def _decode_int(self) -> bytes:
        result_buffer: bytearray = bytearray()
        c = self._get()
        while c != TOKENS.END.value:
            result_buffer += c
            c = self._get()

        return bytes(result_buffer)

    def _decode_dict(self) -> dict[bytes,bytes]:
        c = self._get()
        result = {}
        while c != TOKENS.END.value:
            self._unget()
            key = self._decode_string()
            value = self.decode()
            result[key] = value
            c = self._get()

        return result

    def _decode_string(self) -> bytes:
        length_buffer: bytearray = bytearray()
        string_buffer: bytes = bytes()
        c = self._get()

        while c != TOKENS.SEPERATOR.value:
            length_buffer += c
            c = self._get()

        read_to = self._index + int(length_buffer.decode('utf-8'))
        string_buffer = self._data[self._index:read_to]
        self._index = read_to

        return string_buffer

    def _decode_list(self) -> list[bytes]:
        result = []
        c = self._get()
        while c != TOKENS.END.value:
            self._unget()
            value = self.decode()
            result.append(value)
            c = self._get()

        return result

    def _get(self) -> bytes:
        '''
        Returns one byte from data buffer and move data pointer
        one step forward
        '''

        data = self._data[self._index]
        self._index +=1
        return bytes([data])
    
    def _unget(self) -> None:
        '''
        Move the data pointer back by one
        '''

        assert(self._index > 0)
        self._index -= 1

class Encoder:
    @staticmethod
    def encode(payload) -> bytes:
        if(isinstance(payload,int)):
            return Encoder._encode_int(payload)
        if(isinstance(payload,str)):
            return Encoder._encode_string(payload)
        if(isinstance(payload,list)):
            return Encoder._encode_list(payload)
        if(isinstance(payload,dict)):
            return Encoder._encode_dict(payload)
        if(isinstance(payload,bytes)):
            return Encoder._encode_bytes(payload)
        return b''

    @staticmethod
    def _encode_int(payload: int) -> bytes:
        return str.encode('i' + str(payload) + 'e')

    @staticmethod
    def _encode_bytes(payload: bytes) -> bytes:
        return str(len(payload)).encode() + b':' + payload

    @staticmethod
    def _encode_string(payload: str) -> bytes:
        encoded = str(len(payload)) + ":" + payload
        return str.encode(encoded)

    @staticmethod
    def _encode_dict(payload: dict) -> bytes:
        encoded = b'd'
        for key in sorted(payload.keys()):
            encoded += Encoder.encode(key)
            encoded += Encoder.encode(payload[key])

        encoded += b'e'

        return encoded

    @staticmethod
    def _encode_list(payload: list) -> bytes:
        encoded = b'l'
        for item in payload: 
            encoded += Encoder.encode(item)

        encoded += b'e'

        return encoded
