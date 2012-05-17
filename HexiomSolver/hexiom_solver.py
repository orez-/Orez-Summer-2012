import sys

class HexiomTile:
    pass

class HexiomBoard:
    def __init__(self, side):
        self.board = self.generate_board(side)

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
        board = self.board
        for r, row in enumerate(board):
            toR1 = ""
            toR2 = " "
            for e,elem in enumerate(row):
                if e%2:
                    toR2 += elem+" "
                else:
                    toR1 += elem+" "
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