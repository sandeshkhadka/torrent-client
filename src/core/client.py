from core.message import build_interested
from core.peer import PeerConnection
from core.torrent import Torrent
from core.tracker import Tracker


def start_client(torrent_file):
    torrent = Torrent(torrent_file)
    tracker = Tracker(torrent)
    response = tracker.connect()

    if response.failure:
        print("Tracker error:", response.failure)
        return

    peers = response.peers
    for peer in peers:
        ip = peer[b'ip'].decode()
        port = int(peer[b'port'])

        try:
            peer_conn = PeerConnection(ip, port, torrent.info_hash, tracker.peer_id)
            peer_conn.connect()

            # Send 'interested' message
            if not peer_conn.socket:
                print(f"Failed to connect to {ip}:{port}")
                continue
            peer_conn.socket.sendall(build_interested())
            print(f"Sent INTERESTED to {ip}:{port}")

            # At this point, you wait for UNCHOKE and send REQUEST message...
            # We'll add actual download logic next.

            break
        except Exception as e:
            print(f"Failed to connect to {ip}:{port} — {e}")

