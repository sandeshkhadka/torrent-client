import random
import socket
import string
from struct import unpack

import requests

from core.bencode import Decoder
from core.torrent import Torrent


def generate_peer_id():
    return '-qB4250-' + ''.join(random.choices(string.ascii_letters + string.digits, k=12))

class TrackerResponse:

    def __init__(self, response: dict):
        self.response = response

    @property
    def failure(self):
        if b'failure reason' in self.response:
            return self.response[b'failure reason'].decode('utf-8')
        return None

    @property
    def interval(self) -> int:
        return self.response.get(b'interval', 0)

    @property
    def complete(self) -> int:
        return self.response.get(b'complete', 0)

    @property
    def incomplete(self) -> int:
        return self.response.get(b'incomplete', 0)

    @property
    def peers(self):
        peers = self.response[b'peers']
        if not isinstance(peers, list):
            raise NotImplementedError()
        return peers

    def __str__(self):
        return "incomplete: {incomplete}\n" \
               "complete: {complete}\n" \
               "interval: {interval}\n" \
               "peers: {peers}\n".format(
                   incomplete=self.incomplete,
                   complete=self.complete,
                   interval=self.interval,
                   peers=self.peers)



class Tracker:
    torrent: Torrent
    uploaded: int
    downloaded: int

    def __init__(self, torrent:Torrent):
        self.torrent = torrent
        self.peer_id = generate_peer_id()
        print("Peer id: ", self.peer_id)
        self.uploaded = 0
        self.downloaded = 0
        self.event = 'started'
        self.interval = 0
    def connect(self):
        announce: str = self.torrent.announce.decode("utf-8")
        parms = {
            'info_hash': self.torrent.info_hash,
            'peer_id': self.peer_id,
            'port': 6889,
            'uploaded': self.uploaded,
            'downloaded': self.downloaded,
            'left': self.torrent.total_size - self.downloaded,
            }
        

        # print("Connecting to tracker: ", announce)
        response = requests.get(announce, params=parms)

        data = Decoder(response.text.encode("utf-8")).decode()
        print("Response: ", data)
        if not isinstance(data, dict):
            raise Exception("Invalid response from tracker")
        self.interval = data.get(b'interval', self.interval)
        return TrackerResponse(data)

