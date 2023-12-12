import socket
from _thread import *
from board import Board
import pickle
import time

import socket
from board import Board

class Server:
    def __init__(self, host="localhost", port=5555):
        self.server = host
        self.port = port
        self.server_ip = socket.gethostbyname(self.server)
        self.connections = 0
        self.games = {0: Board(8, 8)}
        self.spectator_ids = []
        self.specs = 0
        self.socket = self.init_socket()
        self.current_id = None

    def init_socket(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((self.server, self.port))
        except socket.error as e:
            print(str(e))
        s.listen()
        print("[START] Waiting for a connection")
        return s



    def read_specs(self):
        try:
            with open("specs.txt", "r") as f:
                for line in f:
                    self.spectator_ids.append(line.strip())
        except:
            print("[ERROR] No specs.txt file found, creating one...")
            open("specs.txt", "w")


    def threaded_client(self, conn, game, spec=False):

        if not spec:
            self.initialize_player(conn, game)
        else:
            self.initialize_spectator(conn, game)

    def initialize_player(self,conn, game):

        name = None
        bo = self.games[game]
        self.current_id = "w" if self.connections % 2 == 0 else "b"
        bo.start_user = self.current_id

        if self.current_id == "b":
            bo.ready = True
            bo.startTime = time.time()

        self.send_data(conn, bo)
        self.connections += 1

        while True:
            self.handle_player_connections(conn, bo, game)

        self.connections -= 1
        self.cleanup_game(game)
        print(f"[DISCONNECT] Player{name} left game {game}.")
        conn.close()

    def initialize_spectator(self,conn, game):

        available_games = list(self.games.keys())
        game_ind = 0
        bo = self.games[available_games[game_ind]]
        bo.start_user = "s"

        self.send_data(conn, bo)

        while True:
            self.handle_spec_connections(conn, game_ind)

        print(f"[DISCONNECT] Spectator left game: {game}")
        specs -= 1
        conn.close()

    def send_data(self,conn, bo):
        data_string = pickle.dumps(bo)
        conn.send(data_string)

    def cleanup_game(self,game):
        try:
            del self.games[game]
            print("[GAME] Game", game, "ended")
        except:
            pass

    def handle_spec_connections(self, conn, game_ind):
        available_games = list(self.games.keys())
        bo = self.games[available_games[game_ind]]
        try:
            data = self.receive_data(conn)
            if not data:
                return

            game_ind = self.process_spectator_data(data, available_games, game_ind)

            bo = self.games[available_games[game_ind]]
            self.send_data(conn, bo)

        except Exception as e:
            print(e)

    def receive_data(self,conn):
        d = conn.recv(128)
        return d.decode("utf-8")

    def process_spectator_data(self,data, available_games, game_ind):
        if data == "forward":
            print("[SPECTATOR] Moved self.games forward")
            game_ind = (game_ind + 1) % len(available_games)
        elif data == "back":
            print("[SPECTATOR] Moved self.games back")
            game_ind = (game_ind - 1) % len(available_games)
        else:
            print("[ERROR] Invalid Game Received from Spectator")
        return game_ind

    def send_data(self,conn, bo):
        send_data = pickle.dumps(bo)
        conn.sendall(send_data)


    def handle_player_connections(self, conn, bo, game):
        if game not in self.games:
            return

        try:
            data = self.receive_data(conn)
            if not data:
                return

            self.process_data(data, bo, game, self.current_id)

            self.send_data(conn, bo)

        except Exception as e:
            print(e)

    def receive_data(self,conn):
        d = conn.recv(8192 * 3)
        return d.decode("utf-8")

    def process_data(self,data, bo, game):
        if "select" in data:
            self.handle_select(data, bo)

        if data in ["winner b", "winner w"]:
            self.handle_winner(data, bo, game)

        if data == "update moves":
            bo.update_moves()

        if "name" in data:
            self.handle_name(data, bo, self.current_id)

        if bo.ready:
            self.handle_time(bo)

    def handle_select(self,data, bo):
        all = data.split(" ")
        col = int(all[1])
        row = int(all[2])
        color = all[3]
        bo.select(col, row, color)

    def handle_winner(self,data, bo, game):
        bo.winner = data.split(" ")[1]
        print(f"[GAME] Player {bo.winner} won in game {game}")

    def handle_name(self,data, bo):
        name = data.split(" ")[1]
        if self.current_id == "b":
            bo.p2Name = name
        elif self.current_id == "w":
            bo.p1Name = name

    def handle_time(self,bo):
        if bo.turn == "w":
            bo.time1 = 900 - (time.time() - bo.startTime) - bo.storedTime1
        else:
            bo.time2 = 900 - (time.time() - bo.startTime) - bo.storedTime2

        

    def send_data(self,conn, bo):
        sendData = pickle.dumps(bo)
        conn.sendall(sendData)


    def run_server(self):
        while True:
            self.read_specs()
            if self.connections < 6:
                conn, addr = s.accept()
                spec = False
                g = self.get_game_id()
                print("[CONNECT] New connection")
                print("[DATA] Number of Connections:", self.connections+1)
                print("[DATA] Number of self.games:", len(self.games))
                start_new_thread(self.threaded_client, (conn,g,spec))

    def get_game_id(self):
        for game in self.games.keys():
            if not self.games[game].ready:
                return game
        return self.create_new_game()

    def create_new_game(self):
        try:
            g = list(self.games.keys())[-1] + 1
        except IndexError:
            g = 0
        self.games[g] = Board(8,8)
        return g

s = Server()
s.run_server()