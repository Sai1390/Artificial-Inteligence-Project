class Board:
    __directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

    def __init__(self):
        # Create the empty board array
        self.__pieces = [[0] * 8 for _ in range(8)]

        # Set up the initial 4 pieces
        self.__pieces[3][4] = 1
        self.__pieces[4][3] = 1
        self.__pieces[3][3] = -1
        self.__pieces[4][4] = -1

    def display(self, time):
        """ Display the board and the statistics of the ongoing game. """
        print("   A B C D E F G H")
        print("  -----------------")
        for y in range(7, -1, -1):
            print(y + 1, '|', end=' ')
            for x in range(8):
                piece = self.__pieces[x][y]
                if piece == -1:
                    print("B", end=' ')
                elif piece == 1:
                    print("W", end=' ')
                else:
                    print(".", end=' ')
            print('|', y + 1)
        print("  -----------------")
        print("   A B C D E F G H\n")

        print("STATISTICS (score / remaining time):")
        print("Black: {} / {}".format(self.count(-1), time[-1]))
        print("White: {} / {}".format(self.count(1), time[1]))

    def count(self, color):
        """ Count the number of pieces of the given color.
        (1 for white, -1 for black, 0 for empty spaces) """
        return sum(row.count(color) for row in self.__pieces)

    def get_squares(self, color):
        """ Get the coordinates (x,y) for all pieces on the board of the given color.
        (1 for white, -1 for black, 0 for empty spaces) """
        squares = []
        for y in range(8):
            for x in range(8):
                if self.__pieces[x][y] == color:
                    squares.append((x, y))
        return squares

    def get_legal_moves(self, color):
        """ Return all the legal moves for the given color.
        (1 for white, -1 for black) """
        moves = set()
        for square in self.get_squares(color):
            new_moves = self.get_moves_for_square(square)
            moves.update(new_moves)
        return list(moves)

    def get_moves_for_square(self, square):
        (x, y) = square
        color = self.__pieces[x][y]
        moves = []
        for direction in self.__directions:
            move = self._discover_move((x, y), direction)
            if move:
                moves.append(move)
        return moves

    def execute_move(self, move, color):
        for x, y in self._get_flips(move, color):
            self.__pieces[x][y] = color

    def _discover_move(self, origin, direction):
        x, y = origin
        color = self.__pieces[x][y]
        flips = []
        for x, y in Board._increment_move(origin, direction):
            if self.__pieces[x][y] == 0 and flips:
                return x, y
            elif self.__pieces[x][y] == color or (self.__pieces[x][y] == 0 and not flips):
                return None
            elif self.__pieces[x][y] == -color:
                flips.append((x, y))

    def _get_flips(self, origin, color):
        flips = [origin]
        for x, y in Board._increment_move(origin, direction):
            if self.__pieces[x][y] == -color:
                flips.append((x, y))
            elif self.__pieces[x][y] == 0:
                break
            elif self.__pieces[x][y] == color and len(flips) > 1:
                return flips
        return []

    @staticmethod
    def _increment_move(move, direction):
        move = (move[0] + direction[0], move[1] + direction[1])
        while 0 <= move[0] < 8 and 0 <= move[1] < 8:
            yield move


def get_col_char(col):
    return chr(ord('A') + col)

def moves_string(moves):
    return ', '.join(move_string(move) for move in moves)

def move_string(move):
    x, y = move
    return "{}{}".format(get_col_char(x), y + 1)

if __name__ == '__main__':
    board = Board()
    board.display([300, 400])  # Replace with actual time values

    print("Black:", moves_string(board.get_legal_moves(-1)))
    print("White:", moves_string(board.get_legal_moves(1)))
