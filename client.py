import socket
import pickle
import time

class Client:
    def __init__(self):
        self.client = self._create_socket()
        self.host = "localhost"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.board = self._connect_and_receive_board()

    def _create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _connect_and_receive_board(self):
        self._connect_to_server()
        board_data = self._receive_data()
        return pickle.loads(board_data)

    def _connect_to_server(self):
        self.client.connect(self.addr)

    def _receive_data(self, buffer_size=4096*8):
        return self.client.recv(buffer_size)

    def disconnect(self):
        self.client.close()

    def send(self, data, pick=False):
        reply = None
        start_time = time.time()
        while time.time() - start_time < 5:
            try:
                self._send_data(data, pick)
                reply = self._receive_and_unpickle_data()
                if reply is not None:
                    break
            except socket.error as e:
                print(e)
        return reply

    def _send_data(self, data, pick):
        if pick:
            self.client.send(pickle.dumps(data))
        else:
            self.client.send(str.encode(data))

    def _receive_and_unpickle_data(self):
        try:
            reply = self._receive_data()
            return pickle.loads(reply)
        except Exception as e:
            print(e)
            return None


