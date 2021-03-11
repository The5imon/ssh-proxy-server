import select
import threading

from enhancements.modules import BaseModule


class BaseTunnelForwarder(BaseModule):
    pass


class TunnelForwarder(BaseTunnelForwarder, threading.Thread):

    def __init__(self, local_ch, remote_ch, session):
        super(TunnelForwarder, self).__init__()
        self.local_ch = local_ch
        self.remote_ch = remote_ch
        self.session = session
        self.run()

    def run(self) -> None:
        self.tunnel()
        self.close()

    def tunnel(self, chunk_size=1024):
        """
        Connect a socket and a SSH channel.
        TODO: Plugin/Interface compatibility can be inserted HERE
        """
        while True:
            r, w, x = select.select([self.local_ch, self.remote_ch], [], [])

            if self.local_ch in r:
                data = self.local_ch.recv(chunk_size)
                if len(data) == 0:
                    break
                self.remote_ch.send(data)

            if self.remote_ch in r:
                data = self.remote_ch.recv(chunk_size)
                if len(data) == 0:
                    break
                self.local_ch.send(data)

    def close(self):
        self.local_ch.close()
        self.remote_ch.close()