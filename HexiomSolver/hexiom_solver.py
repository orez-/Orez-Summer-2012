import sys

class HexiomSpot:
    """ Refer to the location, not the numbered tile placed there. """
    def __init__(self, value):
        def bad_value(value):
            raise ValueError(r"Got '"+value+"', expected ([0-6]L?)|\.|#")
        value = str(value)
        if value == "":
            bad_value(value)
        if value[0] in "0123456":
            self.last_value = 0
            self.value = int(value[0])
            self.locked = len(value) == 2 and value[1] == "L"
            if len(value) > 1 and not self.locked:
                bad_value()
        elif value in ".#":
            self.last_value = -1
            self.value = value
            self.locked = (value == "#")
        else:
            bad_value()

    def recount_neighbors(self):
        count = 0
        for e in self.adjacent:
            if e.last_value != -1:
                count += 1
        self.last_value = count
        return count

    def __str__(self):
        #return str(self.value)
        try:
            int(self.value)
            return str(self.value - self.last_value)
        except ValueError:
            return self.value

class HexiomBoard:
    def __init__(self, side):
        board = self.generate_board_shape(side)
        pattern = ["3L",4,2,4,5,3,".",3,4,"#","#","#",3,".",3,2,1,".","3L"]
        i = 0
        for c in xrange(len(board[0])):
            for r in xrange(len(board)):
                if board[r][c] != "#":
                    if i >= len(pattern):
                        board[r][c] = "."
                        continue
                    board[r][c] = str(pattern[i])
                    i += 1
        self.convert_to_spots(board)

    def swap(self, (r1, c1), (r2, c2)):
        e1 = self.board[r1][c1]
        e2 = self.board[r2][c2]
        if e1.locked or e2.locked:
            return False
        e1.value == e2.value

    def convert_to_spots(self, board):
        self.board = [[HexiomSpot(elem) for elem in row] for row in board]
        for r, row in enumerate(self.board):
            for c, elem in enumerate(row):
                self.build_spot_adj(r, c)

    def build_spot_adj(self, r, c):
        elem = self.board[r][c]
        elem.adjacent = []
        for ra, ca in ((r+1, c), (r-1, c),
                       (r, c-1), (r, c+1),
                       (r + 2*(c%2) - 1, c-1),
                       (r + 2*(c%2) - 1, c+1)):
            if 0 <= ra < len(self.board) and 0 <= ca < len(self.board[0]):
                adj = self.board[ra][ca]
                if str(adj.value) not in ".#":  # it's a number
                    elem.adjacent.append(adj)
        elem.recount_neighbors()

    def generate_board_shape(self, side):
        size = (side * 2) - 1
        toR = []
        for row in xrange(size):
            toR.append([])
            for column in xrange(size):
                char = "."
                # bottom right, bottom left, top right, top left
                if (row*2 + column > (2*side + side//2 - 2) * 2 or
                    row*2 - column > (side + side//2 - 1) * 2 or
                   -row*2 + column >= side + side%2 or
                    row*2 + column + column%2 + side%2 < side):
                    char = "#"
                toR[-1].append(char)
        return toR

    def print_board(self):
        print ""
        board = self.board
        for r, row in enumerate(board):
            toR1 = ""
            toR2 = "  "
            for e,elem in enumerate(row):
                elem = str(elem)
                if e%2:
                    toR2 += elem+"   "
                else:
                    toR1 += elem+"   "
            print toR1
            print toR2

if __name__ == "__main__":
    size = 6
    try:
        size = int(sys.argv[1])
    except:
        pass
    b = HexiomBoard(size)
    b.print_board()