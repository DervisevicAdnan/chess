from enum import Enum

notation_decode = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
}

class color(Enum):
    WHITE = 1
    BLACK = 2

class Play:
    def __init__(self) -> None:
        self.board = Board()
        self.is_check = False
        self.long_castle_allowed = {color.BLACK: True, color.WHITE: True}
        self.short_castle_allowed =  {color.BLACK: True, color.WHITE: True}

    def get_all_valid_moves(self):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if isinstance(self.board.board[i][j],Figure):
                    valid_moves.append(self.get_figure_valid_moves(i,j))

    def get_figure_valid_moves(self, i, j):
        if isinstance(self.board.board[i][j], Pawn):
            return self.get_pawn_valid_moves(i, j)
        elif isinstance(self.board.board[i][j], Rook):
            return self.get_rook_valid_moves(i, j)
        elif isinstance(self.board.board[i][j], Bishop):
            return self.get_bishop_valid_moves(i, j)
        elif isinstance(self.board.board[i][j], Knight):
            return self.get_knight_valid_moves(i, j)
        elif isinstance(self.board.board[i][j], King):
            return self.get_king_valid_moves(i, j)
        elif isinstance(self.board.board[i][j], Queen):
            return self.get_queen_valid_moves(i, j)
        pass

    def get_pawn_valid_moves(self, x, y):
        valid = []
        if self.board.board[x][y].color == color.BLACK:
            if x < 7:
                if isinstance(self.board.board[x + 1][y], EmptyField):
                    valid.append((x, y, x + 1, y))
                if y < 7 and isinstance(self.board.board[x + 1][y + 1],Figure) and self.board.board[x + 1][y + 1].color != color.BLACK:
                    valid.append((x, y, x + 1, y + 1))
                if y > 0 and isinstance(self.board.board[x + 1][y - 1],Figure) and self.board.board[x + 1][y - 1].color != color.BLACK:
                    valid.append((x, y, x + 1, y - 1))
        else:
            if x > 0:
                if not isinstance(self.board.board[x - 1][y], Figure):
                    valid.append((x, y, x - 1, y))
                if y < 7 and isinstance(self.board.board[x - 1][y + 1],Figure) and self.board.board[x - 1][y + 1].color != color.BLACK:
                    valid.append((x, y, x - 1, y + 1))
                if y > 0 and isinstance(self.board.board[x - 1][y - 1],Figure) and self.board.board[x - 1][y - 1].color != color.BLACK:
                    valid.append((x, y, x - 1, y - 1))
        return valid

    def get_rook_valid_moves(self, x, y):
        valid = []
        for i in range(x + 1, 8):
            if isinstance(self.board.board[i][y], EmptyField):
                valid.append((x, y, i, y))
            elif isinstance(self.board.board[i][y], Figure) and self.board.board[i][y].color != self.board.board[x][y].color:
                valid.append((x, y, i, y))
                break
            else:
                break
        for i in range(x - 1, -1, -1):
            if isinstance(self.board.board[i][y], EmptyField):
                valid.append((x, y, i, y))
            elif isinstance(self.board.board[i][y], Figure) and self.board.board[i][y].color != self.board.board[x][y].color:
                valid.append((x, y, i, y))
                break
            else:
                break
        for j in range(y + 1, 8):
            if isinstance(self.board.board[x][j], EmptyField):
                valid.append((x, y, x, j))
            elif isinstance(self.board.board[x][j], Figure) and self.board.board[x][j].color != self.board.board[x][y].color:
                valid.append((x, y, x, j))
                break
            else:
                break
        for j in range(y - 1, -1, -1):
            if isinstance(self.board.board[x][j], EmptyField):
                valid.append((x, y, x, j))
            elif isinstance(self.board.board[x][j], Figure) and self.board.board[x][j].color != self.board.board[x][y].color:
                valid.append((x, y, x, j))
                break
            else:
                break
        return valid
    
    def get_bishop_valid_moves(self, x, y):
        valid = []
        for i in range(1, min(8 - x, 8 - y)):
            if isinstance(self.board.board[x + i][y + i], EmptyField):
                valid.append((x, y, x + i, y + i))
            elif isinstance(self.board.board[x + i][y + i], Figure) and self.board.board[x + i][y + i].color != self.board.board[x][y].color:
                valid.append((x, y, x + i, y + i))
                break
            else:
                break
        for i in range(1, min(x, y) + 1):
            if isinstance(self.board.board[x - i][y - i], EmptyField):
                valid.append((x, y, x - i, y - i))
            elif isinstance(self.board.board[x - i][y - i], Figure) and self.board.board[x - i][y - i].color != self.board.board[x][y].color:
                valid.append((x, y, x - i, y - i))
                break
            else:
                break
        for i in range(1, min(x, 8 - y)):
            if isinstance(self.board.board[x - i][y + i], EmptyField):
                valid.append((x, y, x - i, y + i))
            elif isinstance(self.board.board[x - i][y + i], Figure) and self.board.board[x - i][y + i].color != self.board.board[x][y].color:
                valid.append((x, y, x - i, y + i))
                break
            else:
                break
        for i in range(1, min(8 - x, y)):
            if isinstance(self.board.board[x + i][y - i], EmptyField):
                valid.append((x, y, x + i, y - i))
            elif isinstance(self.board.board[x + i][y - i], Figure) and self.board.board[x + i][y - i].color != self.board.board[x][y].color:
                valid.append((x, y, x + i, y - i))
                break
            else:
                break
        return valid
    
    def get_knight_valid_moves(self, x, y):
        possible = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        valid = []
        for i in possible:
            tmp_x = x + i[0]
            tmp_y = y + i[1]
            if tmp_x >= 0 and tmp_x < 8 and tmp_y >= 0 and tmp_y < 8:
                if isinstance(self.board.board[tmp_x][tmp_y], EmptyField):
                    valid.append((x, y, tmp_x, tmp_y))
                elif isinstance(self.board.board[tmp_x][tmp_y], Figure) and self.board.board[tmp_x][tmp_y].color != self.board.board[x][y].color:
                    valid.append((x, y, tmp_x, tmp_y))
        return valid
    
    def get_king_valid_moves(self, x, y):
        pass

    def get_queen_valid_moves(self, x, y):
        valid = []
        valid.append(self.get_rook_valid_moves(x, y))
        valid.append(self.get_bishop_valid_moves(x, y))
        return valid

class Board:

    '''
    
    board 
    
    bR bN bB bQ bK bB bN bR
    bP bP bP bP bP bP bP bP



    
    wP wP wP wP wP wP wP wP
    wR wN wB wQ wK wB wN wR

    '''

    def __init__(self):
        starting_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        self.board = []
        self.set_position(starting_FEN)

    def set_position(self, fen_notation):
        self.board = [[EmptyField() for _ in range(8)] for _ in range(8)]
        self.decode_FEN(fen_notation)

    def print(self):
        row_notation = "   "
        for i in range(8):
            row_notation += "  " + chr(ord('a') + i) + "  "
        print(row_notation)
        row_line = "  " + "-" * (len(row_notation) - 2)
        print(row_line)
        for i in range(8):
            row = str(8 - i) + " |"
            for j in range(8):
                row += " " + self.board[i][j].to_string() + " |"
            print(row)
            print(row_line)

    def decode_FEN(self, fen_notation):
        board_row = 0
        board_col = 0
        for character in fen_notation:
            if character == '/':
                board_row += 1
                board_col = 0
            elif character.isdigit():
                for _ in range(int(character)):
                    self.board[board_row][board_col] = EmptyField()
                    board_col += 1
            else:
                if character == 'p':
                    self.board[board_row][board_col] = Pawn(color.BLACK)
                elif character == 'r':
                    self.board[board_row][board_col] = Rook(color.BLACK)
                elif character == 'n': 
                    self.board[board_row][board_col] = Knight(color.BLACK)
                elif character == 'b':
                    self.board[board_row][board_col] = Bishop(color.BLACK)
                elif character == 'q':
                    self.board[board_row][board_col] = Queen(color.BLACK)
                elif character == 'k':
                    self.board[board_row][board_col] = King(color.BLACK)
                elif character == 'R':
                    self.board[board_row][board_col] = Rook(color.WHITE)
                elif character == 'N': 
                    self.board[board_row][board_col] = Knight(color.WHITE)
                elif character == 'B':
                    self.board[board_row][board_col] = Bishop(color.WHITE)
                elif character == 'Q':
                    self.board[board_row][board_col] = Queen(color.WHITE)
                elif character == 'K':
                    self.board[board_row][board_col] = King(color.WHITE)
                elif character == 'P':
                    self.board[board_row][board_col] = Pawn(color.WHITE)
                board_col += 1

    def encode_FEN(self):
        fen_notation=""
        for row in self.board:
            empty_field_counter = 0
            for square in row:
                if isinstance(square, EmptyField):
                    empty_field_counter += 1
                else:
                    if empty_field_counter > 0:
                        fen_notation += str(empty_field_counter)
                        empty_field_counter = 0
                    if square.color == 1:
                        if isinstance(square, Pawn):
                            fen_notation += 'P'
                        elif isinstance(square, Rook):
                            fen_notation += 'R'
                        elif isinstance(square, Knight):
                            fen_notation += 'K'
                        elif isinstance(square, Bishop):
                            fen_notation += 'B'
                        elif isinstance(square, King):
                            fen_notation += 'K'
                        elif isinstance(square, Queen):
                            fen_notation += 'Q'
                    else:
                        if isinstance(square, Pawn):
                            fen_notation += 'p'
                        elif isinstance(square, Rook):
                            fen_notation += 'r'
                        elif isinstance(square, Knight):
                            fen_notation += 'k'
                        elif isinstance(square, Bishop):
                            fen_notation += 'b'
                        elif isinstance(square, King):
                            fen_notation += 'k'
                        elif isinstance(square, Queen):
                            fen_notation += 'q'
            if empty_field_counter > 0:
                    fen_notation += str(empty_field_counter)
                    empty_field_counter = 0
            fen_notation += '/'
        return fen_notation

class Field:
    def __init__(self) -> None:
        pass

    def to_string(self):
        pass

class EmptyField(Field):
    def __init__(self) -> None:
        super().__init__()
    
    def to_string(self):
        return "  "

class Figure(Field):
    def __init__(self, color) -> None:
        super().__init__()
        self.color = color

class Rook(Figure):
    def __init__(self, color) -> None:
        super().__init__(color)
    
    def to_string(self):
        return ("w" if self.color == color.WHITE else "b") + "R"

class Bishop(Figure):
    def __init__(self, color) -> None:
        super().__init__(color)

    def to_string(self):
        return ("w" if self.color == color.WHITE else "b") + "B"

class Knight(Figure):
    def __init__(self, color) -> None:
        super().__init__(color)
    
    def to_string(self):
        return ("w" if self.color == color.WHITE else "b") + "N"

class King(Figure):
    def __init__(self, color) -> None:
        super().__init__(color)
    
    def to_string(self):
        return ("w" if self.color == color.WHITE else "b") + "K"

class Queen(Figure):
    def __init__(self, color) -> None:
        super().__init__(color)

    def to_string(self):
        return ("w" if self.color == color.WHITE else "b") + "Q"

class Pawn(Figure):
    def __init__(self, color) -> None:
        super().__init__(color)

    def to_string(self):
        return ("w" if self.color == color.WHITE else "b") + "P"

b = Board()
b.print()

print('\n')

print(b.encode_FEN())

print('\n')
