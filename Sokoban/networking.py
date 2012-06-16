import socket
import threading
import select
from Queue import Queue

from board import Player, Board

HOST = socket.gethostname()
PORT = 11173
ADDR = (HOST,PORT)

MAX_PACKET_LENGTH = 1024
RS = chr(30)

class Server(threading.Thread):
    CLOSED = 1
    PLAYER = 2
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(ADDR)
        self.done = False
        self.board = Board([[]])
        self.slots = [{"type":Server.CLOSED} for _ in xrange(2)]

    def run(self):
        self.sock.listen(2)
        while not self.done:
            inputs = [x["conn"] for x in self.slots if x.has_key("conn")] + [self.sock]
            # blocks until someone connects or a client sends a message
            ready, _, _ = select.select(inputs, [], [], 0.5)
            for c in ready:
                if c == self.sock:    # new player
                    conn, _ = c.accept()
                    x = self.get_next_slot()
                    other_player = None
                    if x:
                        other_player = self.slots[0]["player"]
                    self.slots[x] = {"type":Server.PLAYER, "conn":conn,
                        "player":Player(self.board, (0,0), other_player),
                        "buffer":""}
                    if x:
                        self.broadcast("START")  # TODO: probably want to send which map we're playing on
                else:   # returning player's command
                    sender = self.get_sender(c)
                    message = self.slots[sender]["conn"].recv(MAX_PACKET_LENGTH)
                    if not message:  # close connection
                        c.close()
                    else:   # a real command
                        sender = self.get_sender(c)
                        self.slots[sender]["buffer"] += message

                        while RS in self.slots[sender]["buffer"]:
                            term, _, self.slots[sender]["buffer"] = self.slots[sender]["buffer"].partition(RS)
                            self.handle_input(sender, term)

    def handle_input(self, slot, message):
        msg = message.split(" ")
        if msg[0] == "MOVED":
            self.slots[slot]["player"].move(int(msg[1]), int(msg[2]))
            self.broadcast(' '.join((msg[0], str(slot), msg[1], msg[2])))

    def broadcast(self, msg):
        for x in self.slots:
            if "conn" in x:
                x["conn"].send(msg+RS)

    def process_received(self, msg):
        pass

    def stop(self):
        self.done = True

    def get_sender(self, c):
        for i,x in enumerate(self.slots):
            if x.has_key("conn"):
                if x["conn"] == c:
                    return i

    def get_next_slot(self):
        for i, x in enumerate(self.slots):
            if x["type"] == Server.CLOSED:
                return i

class Client(threading.Thread):
    def __init__(self, main, host=None):
        self.main = main
        if host is None:
            self.ADDR=(HOST, PORT)
        else:
            self.ADDR=(host, PORT)
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.msgs = Queue()
        self.done = False
        self.recv_buf = ''

    def run(self):
        try:
            self.sock.connect(self.ADDR)
        except IOError:
            print "Couldn't connect"
            self.main.change_screen("no connect")
            return
        self.sock.settimeout(0.5)
        while not self.done:
            while not self.done and self.recv_buf.find(RS) == -1:
                try:
                    message = self.sock.recv(MAX_PACKET_LENGTH)
                except socket.timeout:
                    continue
                if not message:
                    # an empty string indicates that the client has
                    # closed their connection
                    #print "closed connection"
                    self.done = True
                    self.sock.close()
                    break
                else:
                    self.recv_buf += message
                    print message
            if not self.done:
                term, _, self.recv_buf = self.recv_buf.partition(RS) 
                self.process_received(term)

    def stop(self):
        self.done = True

    def send(self, msg):
        buf = msg + RS
        while buf:
            self.sock.send(buf[:MAX_PACKET_LENGTH])
            buf = buf[MAX_PACKET_LENGTH:]


    def process_received(self, message):
        msg = message.split(" ")
        if msg[0] == "MOVED":
            person, dx, dy = map(int, msg[1:])
            p = self.main.ui.player1
            if person:
                p = self.main.ui.player2
            p.move(dx, dy)
        if msg[0] == "START":
            self.main.change_screen("game")
