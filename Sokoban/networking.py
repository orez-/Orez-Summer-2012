import socket
import threading
import select
from Queue import Queue

from board import Player, Board
from constants import RS, US, get_noun
from level_save import LevelLoad

HOST = socket.gethostname()
PORT = 11173
ADDR = (HOST,PORT)

MAX_PACKET_LENGTH = 1024

class UserSlot(object):
    OPEN = object()  # uses less memory than an integer, actually.
    PLAYER = object()

    def __init__(self, *args):
        self.set_open()

    def parse_buffer(self):
        while RS in self.buffer:
            term, _, self.buffer = self.buffer.partition(RS)
            yield term

    def set_open(self):
        self._status = UserSlot.OPEN
        self.conn = None
        self.buffer = ""
        self.player = None

    def new_player(self, connection, teammate=None):
        self.set_connection(connection)
        self.player = Player(None, (0, 0), False, teammate)

    def set_connection(self, connection, safe_mode=True):
        assert((not safe_mode) or self.is_open())
        self.conn = connection
        self._status = UserSlot.PLAYER

    def is_open(self):
        return self._status == UserSlot.OPEN

    def send(self, *msg):
        message = ' '.join(map(str, msg))
        self.conn.send(message + RS)


class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(ADDR)
        self.done = False
        self.board = None
        self.boardname = None
        self.slots = [UserSlot() for _ in xrange(2)]
        self.pending_connections = []

        self.daemon = True
        self.polls = {}
        self.poll_commands = {"restart": self.cmd_restart}

    def cmd_restart(self):
        self.broadcast("RESTART")
        self.load_level()

    def run(self):
        self.sock.listen(2)
        while not self.done:
            inputs = [x.conn for x in self.slots if not x.is_open()] + [x.conn for x in self.pending_connections] + [self.sock]
            # blocks until someone connects or a client sends a message
            ready, _, _ = select.select(inputs, [], [], 0.5)
            for c in ready:
                if c == self.sock:    # new player
                    self.player_join(c)
                    continue
                sender = None
                for sender, x in enumerate(self.pending_connections):
                    if x.conn == c:
                        message = c.recv(MAX_PACKET_LENGTH)
                        if not message:
                            c.close()
                            del self.pending_connections[sender]
                        else:
                            x.buffer += message
                            for msg in x.parse_buffer():
                                if msg == "SOKOPING":  # just checking
                                    x.send("SOKOPONG")
                                    c.close()
                                    del self.pending_connections[sender]
                                elif msg == "JOIN":  # can I play?
                                    self.slots[1].new_player(c,
                                        self.slots[0].player)
                                    for j in self.pending_connections:
                                        if j != x:  # the game is full to all
                                            j.send("FULL")  # except x
                                            j.conn.close()
                                    self.pending_connections = []
                                    self.broadcast("START")
                                else:
                                    print "Unexpected message for a pending connection:", msg
                        break
                    sender = None
                if sender is None:
                    # returning player's command
                    message = c.recv(MAX_PACKET_LENGTH)
                    sender = self.get_sender(c)
                    if not message:  # close connection
                        c.close()  # TODO: probably want more in here
                        self.slots[sender].set_open()
                    else:   # a real command
                        self.slots[sender].buffer += message
                        for msg in self.slots[sender].parse_buffer():
                            self.handle_input(sender, msg)

    def player_join(self, c):
        conn, _ = c.accept()
        x = self.get_next_slot()
        if x:
            us = UserSlot()
            us.set_connection(conn)
            self.pending_connections.append(us)
        elif x is not None:
            self.slots[x].new_player(conn)
        else:  # out of space
            conn.send("FULL" + RS)
            print "out of space"  # i have a hunch that this line is crucial
            conn.close()

    def handle_input(self, slot, message):
        msg = message.split(" ")
        if msg[0] == "MOVED":
            dx, dy = map(int, msg[1:])
            p = self.slots[slot].player
            if p.move(dx, dy):
                self.broadcast(msg[0], str(slot), msg[1], msg[2])
        elif msg[0] == "MSG":
            if msg[1][:1] == "/":  # /commands
                command = msg[1][1:]
                if command in self.poll_commands:
                    if command in self.polls and self.polls[command] != slot:
                        del self.polls[command]
                        self.poll_commands[command]()  # maybe pass some params
                    else:
                        self.polls[command] = slot
                        self.broadcast("MSG 3 Your " + US + "0" + str(slot) +
                            get_noun() + US + "03 has requested a " + command +
                            ". Type " + US + "0" + str(int(not slot)) + "/" +
                            command + US + "03 to allow.")
                else:
                    if command == "help":
                        self.slots[slot].send("MSG 2 The following commands are available: " +
                            ', '.join(self.poll_commands))
                    else:
                        self.slots[slot].send("MSG 2 Unknown command:", command)
            else:
                self.broadcast(msg[0], slot, *msg[1:])
        elif msg[0] == "HELP":
            self.slots[int(msg[1])].send("MSG 3 ? " + US + "02" + ' '.join(msg[2:]))
        elif msg[0] == "LEVELOFF":  # propagate
            self.slots[not slot].send(*msg)
        elif msg[0] == "LEVELACC":  # propagate
            self.slots[not slot].send(*msg)
        elif msg[0] == "LEVELULD":
            self.slots[not slot].send(*msg)
        elif msg[0] == "STARTGAME":  # time to start the game!!!
            self.broadcast("STARTGAME", msg[1])
            self.load_level(msg[1])

    def load_level(self, name=None):
        if name is None:
            name = self.boardname
        loc, self.board = LevelLoad.load_level(name)
        self.boardname = name
        for slot in self.slots:
            slot.player.pos = loc
            slot.player.board = self.board

    def broadcast(self, *msg):
        for x in self.slots:
            if not x.is_open():
                x.send(*msg)

    def process_received(self, msg):
        pass

    def stop(self):
        self.done = True

    def get_sender(self, c):
        for i,x in enumerate(self.slots):
            if x.conn == c:
                return i
        print "Server.get_sender: I couldn't find the guy you're looking for, this is really bad."

    def get_next_slot(self):
        for i, x in enumerate(self.slots):
            if x.is_open():
                return i
        return None


class Client(threading.Thread):
    def __init__(self, main, host=None):
        self.main = main
        if host is None:
            host = HOST
        self.ADDR = (host, PORT)
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.outmsgs = Queue()
        self.done = False
        self.recv_buf = ''
        self.connected = False
        self.daemon = True

    def run(self):
        try:
            self.sock.connect(self.ADDR)
        except IOError:
            print "Couldn't connect"
            self.main.change_screen("no connect")
            return
        self.sock.settimeout(0.5)
        while not self.outmsgs.empty():
            self.send(self.outmsgs.get(), True)
        self.connected = True
        while not self.done:
            while not self.outmsgs.empty():
                self.send(self.outmsgs.get())
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

    def send(self, msg, force=False):
        if self.connected or force:
            buf = msg + RS
            while buf:
                self.sock.send(buf[:MAX_PACKET_LENGTH])
                buf = buf[MAX_PACKET_LENGTH:]
        else:
            self.outmsgs.put(msg)

    def process_received(self, message):
        msg = message.split(" ")
        if msg[0] == "MOVED":
            person, dx, dy = map(int, msg[1:])
            p = self.main.ui.player1
            if person:
                p = self.main.ui.player2
            p.move(dx, dy)
        elif msg[0] == "START":
            self.main.change_screen("level select")
        elif msg[0] == "MSG":
            self.main.ui.chatbox.message(int(msg[1]), ' '.join(msg[2:]))
        elif msg[0] == "RESTART":
            self.main.restart()
        elif msg[0] == "LEVELOFF":  # make sure you're correct
            filename, hashh = msg[1:3]
            self.main.ui.set_suggestion(filename, hashh)
        elif msg[0] == "LEVELACC":  # Level accepted: start?
            send_map, filename, hashh = msg[1:]
            print msg[1:]
            if int(send_map):
                with open("data/maps/" + filename + ".skb", "r") as f:
                    self.main.send_msg("LEVELULD " + filename + " " + f.read())
                    print "Message sent????"
            else:
                self.main.send_msg("STARTGAME " + filename)
        elif msg[0] == "LEVELULD":  # Level uploaded: save it!
            print "got a level ULD"
            filename = msg[1]
            full_filename = LevelLoad.full_path(filename)
            data = ' '.join(msg[2:])
            if LevelLoad.file_exists(full_filename):
                LevelLoad.archive(full_filename)
            with open(full_filename, "w") as f:
                f.write(data)
            self.main.send_msg("STARTGAME " + filename)
        elif msg[0] == "STARTGAME":  # everyone's ready!
            print msg
            self.main.change_screen("game", level=msg[1])
        elif msg[0] == "FULL":  # couldn't join
            pass
        elif msg[0] == "SOKOPONG":
            pass


class TestConnection(threading.Thread):
    def __init__(self, host, callback):
        super(TestConnection, self).__init__()
        self.ADDR = (host, PORT)
        self.cb = callback
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.done = False
        self.daemon = True

    def stop(self):
        self.done = True

    def run(self):
        self.cb("POLLING")
        self.done = False
        try:
            self.sock.connect(self.ADDR)
        except IOError:  # couldn't connect
            self.cb("BAD")
            return
        self.sock.settimeout(0.5)
        self.sock.send("SOKOPING" + chr(30))
        while not self.done:
            try:
                message = self.sock.recv(MAX_PACKET_LENGTH)
            except socket.timeout:
                continue
            except IOError:
                self.cb("BAD")
                return
            if not message:  # done i guess.
                self.cb(None)
                return
            else:
                while message:
                    msg, _, message = message.partition(chr(30))
                    if msg in ("FULL", "SOKOPONG"):
                        self.cb(msg)
                        return
                    else:
                        print "Unrecognized message:", msg
