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
    WHITE = 0
    BLACK = 1

class Play:
    def __init__(self) -> None:
        self.board = Board()
    

class Board:

    '''
    
    board 
    
    bR bN bB bQ bK bB bN bR
    bP bP bP bP bP bP bP bP



    
    wP wP wP wP wP wP wP wP
    wR wN wB wQ wK wB wN wR

    '''

    def __init__(self):
        starting_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.board = []
        self.set_position(starting_FEN)
        
        self.kings_positions = {color.BLACK: (8, 8), color.WHITE: (8, 8)}

        self.valid_moves_by_color = { color.BLACK: [], color.WHITE: []}
        self.check_moves = { color.BLACK: [], color.WHITE: []}
        self.is_check = {color.BLACK: False, color.WHITE: False}
        self.long_castle_allowed = {color.BLACK: True, color.WHITE: True}
        self.short_castle_allowed =  {color.BLACK: True, color.WHITE: True}

        self.guarded_pieces = {color.BLACK: set(), color.WHITE: set()}

        self.checkmate = {color.BLACK: False, color.WHITE: False}
        self.draw = False

        self.active_color_move = color.WHITE
        self.half_moves = 0
        self.moves_num = 1

        self.update_valid_moves()
        # ideja je da previous_moves bude lista tuplova (Figure, prev_x, prev_y, new_x, new_y)
        # self.previous_moves = []

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

        split = fen_notation.split()
        board_position = split[0]
        active_color_move = split[1]
        if active_color_move == 'w':
            self.active_color_move = color.WHITE
        else:
            self.active_color_move = color.BLACK
        castling = split[2]

        # Mogucnosti [('-'), ('KQkq'), ('Kkq'), ('Qkq'), ('KQk'), ('KQq'), ('KQ'), ('kq'), ('Kk'), ('Kq'), ('Qk'), ('Qq'), ('K'), ('Q'), ('k'), ('q')]

        # Mislim da nije potrebno, postavlja se u konstruktoru
        self.long_castle_allowed = {color.BLACK: False, color.WHITE: False}
        self.short_castle_allowed =  {color.BLACK: False, color.WHITE: False}
        
        if 'K' in castling:
            self.short_castle_allowed[color.WHITE] = True
        if 'Q' in castling:
            self.long_castle_allowed[color.WHITE] = True
        if 'k' in castling:
            self.short_castle_allowed[color.BLACK] = True
        if 'q' in castling: 
            self.long_castle_allowed[color.BLACK] = True

        en_passant = split[3]

        if en_passant[0] != '-':
            file = notation_decode.get(en_passant[0], "Invalid move")
            rank = 8 - int(en_passant[1])
            self.board[rank][file] = EnPassantEmptyField()

        # Ovo je za brojanje koliko je proslo od zadnjeg saha ili uzimanja figure -> kasnije dodat kad se omoguci igranje
        self.half_moves = int(split[4])
        # Ovo je za brojanje ukupnih poteza, update the poslije poteza crnog
        self.moves_num = int(split[5])

        board_row = 0
        board_col = 0
        for character in board_position:
            if character == '/':
                board_row += 1
                board_col = 0
            elif character.isdigit():
                for _ in range(int(character)):
                    if isinstance(self.board[board_row][board_col], EnPassantEmptyField):
                        continue
                    else:
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
        en_passant_field="-"
        for row_index, row in enumerate(self.board):
            empty_field_counter = 0
            for col_index, square in enumerate(row):
                if isinstance(square, EnPassantEmptyField):
                    file = ""
                    for key, val in notation_decode.items():
                        if val == col_index:
                            file = key
                    en_passant_field = file + str(8 - row_index)
                    empty_field_counter += 1
                elif isinstance(square, EmptyField):
                    empty_field_counter += 1
                else:
                    if empty_field_counter > 0:
                        fen_notation += str(empty_field_counter)
                        empty_field_counter = 0
                    if square.color == color.WHITE:
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
            if row_index != 7:
                fen_notation += '/'
        
        if self.active_color_move == color.WHITE:
            fen_notation += ' ' + 'w'
        else:
            fen_notation += ' ' + 'b'
        
        castle_rights = ""
        if self.short_castle_allowed[color.WHITE] == True:
            castle_rights += 'K'
        if self.long_castle_allowed[color.WHITE] == True:
            castle_rights += 'Q'
        if self.short_castle_allowed[color.BLACK] == True:
            castle_rights += 'k'
        if self.long_castle_allowed[color.BLACK] == True:
            castle_rights += 'q'  
        if len(castle_rights) == 0:
            castle_rights += '-'

        fen_notation += ' ' + castle_rights + ' ' + en_passant_field + ' ' + str(self.half_moves) + ' ' + str(self.moves_num)
        return fen_notation
    
    def get_all_valid_moves(self):
        return self.valid_moves_by_color[color.BLACK] + self.valid_moves_by_color[color.WHITE]

    def update_valid_moves(self):
        self.valid_moves_by_color = { color.BLACK: [], color.WHITE: []}
        self.guarded_pieces =  {color.BLACK: set(), color.WHITE: set()}
        for i in range(8):
            for j in range(8):
                if isinstance(self.board[i][j], King):
                    self.kings_positions[self.board[i][j].color] = (i, j)
                elif isinstance(self.board[i][j], Figure):
                    self.valid_moves_by_color[self.board[i][j].color].extend(self.get_figure_valid_moves(i,j))
                    
        self.valid_moves_by_color[color.BLACK].extend(self.get_figure_valid_moves(*self.kings_positions[color.BLACK]))
        self.valid_moves_by_color[color.WHITE].extend(self.get_figure_valid_moves(*self.kings_positions[color.WHITE]))
        for col in [color.WHITE, color.BLACK]:
            if len(self.valid_moves_by_color[col]) == 0 and not self.checkmate[col]:
                self.draw = True
        pass

    def get_figure_valid_moves(self, i, j):
        if isinstance(self.board[i][j], Pawn):
            return self.get_pawn_valid_moves(i, j)
        elif isinstance(self.board[i][j], Rook):
            return self.get_rook_valid_moves(i, j)
        elif isinstance(self.board[i][j], Bishop):
            return self.get_bishop_valid_moves(i, j)
        elif isinstance(self.board[i][j], Knight):
            return self.get_knight_valid_moves(i, j)
        elif isinstance(self.board[i][j], King):
            return self.get_king_valid_moves(i, j)
        elif isinstance(self.board[i][j], Queen):
            return self.get_queen_valid_moves(i, j)
        pass

    def get_pawn_valid_moves(self, x, y):
        valid = []
        if self.board[x][y].color == color.BLACK:
            if x < 7:
                if isinstance(self.board[x + 1][y], EmptyField):
                    valid.append((x, y, x + 1, y))
                    if x == 1 and isinstance(self.board[x + 2][y], EmptyField):
                        valid.append((x, y, x + 2, y))
                if y < 7 and isinstance(self.board[x + 1][y + 1], Figure):
                    if self.board[x + 1][y + 1].color != color.BLACK:
                        if isinstance(self.board[x + 1][y + 1], King):
                            self.check_moves[color.BLACK].append((x, y, x + 1, y + 1))
                        else:
                            valid.append((x, y, x + 1, y + 1))
                    else:
                        self.guarded_pieces[self.board[x][y].color].add((x + 1, y + 1))
                if y > 0 and isinstance(self.board[x + 1][y - 1], Figure) and self.board[x + 1][y - 1].color != color.BLACK:
                    if self.board[x + 1][y - 1].color != color.BLACK:
                        if isinstance(self.board[x + 1][y - 1], King):
                            self.check_moves[color.BLACK].append((x, y, x + 1, y - 1))
                        else:
                            valid.append((x, y, x + 1, y - 1))
                    else:
                        self.guarded_pieces[self.board[x][y].color].add((x + 1, y - 1))
                if x == 4:
                    if y < 7 and isinstance(self.board[x + 1][y + 1], EnPassantEmptyField):  # self.valid_en_passant(self.board[x][y], x, y + 1):
                        valid.append((x, y, x + 1, y + 1))
                    if y > 0 and isinstance(self.board[x + 1][y - 1], EnPassantEmptyField):  # self.valid_en_passant(self.board[x][y], x, y - 1):
                        valid.append((x, y, x + 1, y - 1))
        else:
            if x > 0:
                if not isinstance(self.board[x - 1][y], Figure):
                    valid.append((x, y, x - 1, y))
                    if x == 6 and isinstance(self.board[x - 2][y], EmptyField):
                        valid.append((x, y, x - 2, y))
                if y < 7 and isinstance(self.board[x - 1][y + 1], Figure): # and abs(x - self.previous_moves[-1][0]) == 2:
                    if self.board[x - 1][y + 1].color != color.WHITE:
                        if isinstance(self.board[x - 1][y + 1], King):
                            self.check_moves[color.WHITE].append((x, y, x - 1, y + 1))
                        else:
                            valid.append((x, y, x - 1, y + 1))
                    else:
                        self.guarded_pieces[self.board[x][y].color].add((x - 1, y + 1))
                if y > 0 and isinstance(self.board[x - 1][y - 1], Figure):
                    if self.board[x - 1][y - 1].color != color.WHITE:
                        if isinstance(self.board[x - 1][y - 1], King):
                            self.check_moves[color.WHITE].append((x, y, x - 1, y - 1))
                        else:
                            valid.append((x, y, x - 1, y - 1))
                    else:
                        self.guarded_pieces[self.board[x][y].color].add((x - 1, y - 1))
                if x == 3:
                    if y < 7 and isinstance(self.board[x - 1, y + 1], EnPassantEmptyField):   # self.valid_en_passant(self.board[x][y], x, y + 1):
                        valid.append(x, y, x - 1, y + 1)
                    if y > 0 and isinstance(self.board[x - 1, y - 1], EnPassantEmptyField):   # self.valid_en_passant(self.board[x][y], x, y - 1):
                        valid.append(x, y, x - 1, y - 1)
        return valid

    def get_rook_valid_moves(self, x, y):
        valid = []
        for i in range(x + 1, 8):
            if isinstance(self.board[i][y], EmptyField):
                valid.append((x, y, i, y))
            elif isinstance(self.board[i][y], Figure):
                if self.board[i][y].color != self.board[x][y].color:
                    if isinstance(self.board[i][y], King):
                        self.check_moves[self.board[x][y].color].append((x, y, i, y))
                    else:
                        valid.append((x, y, i, y))
                else:
                    self.guarded_pieces[self.board[x][y].color].add((i, y))
                break
            else:
                break
        for i in range(x - 1, -1, -1):
            if isinstance(self.board[i][y], EmptyField):
                valid.append((x, y, i, y))
            elif isinstance(self.board[i][y], Figure):
                if self.board[i][y].color != self.board[x][y].color:
                    if isinstance(self.board[i][y], King):
                        self.check_moves[self.board[x][y].color].append((x, y, i, y))
                    else:
                        valid.append((x, y, i, y))
                else:
                    self.guarded_pieces[self.board[x][y].color].add((i, y))
                break
            else:
                break
        for j in range(y + 1, 8):
            if isinstance(self.board[x][j], EmptyField):
                valid.append((x, y, x, j))
            elif isinstance(self.board[x][j], Figure):
                if self.board[x][j].color != self.board[x][y].color:
                    if isinstance(self.board[x][j], King):
                        self.check_moves[self.board[x][j].color].append((x, y, x, j))
                    else:
                        valid.append((x, y, x, j))
                else:
                    self.guarded_pieces[self.board[x][y].color].add((x, j))
                break
            else:
                break
        for j in range(y - 1, -1, -1):
            if isinstance(self.board[x][j], EmptyField):
                valid.append((x, y, x, j))
            elif isinstance(self.board[x][j], Figure):
                if self.board[x][j].color != self.board[x][y].color:
                    if isinstance(self.board[x][j], King):
                        self.check_moves[self.board[x][j].color].append((x, y, x, j))
                    else:
                        valid.append((x, y, x, j))
                else:
                    self.guarded_pieces[self.board[x][y].color].add((x, j))
                break
            else:
                break
        return valid
    
    def get_bishop_valid_moves(self, x, y):
        valid = []
        for i in range(1, min(8 - x, 8 - y)):
            if isinstance(self.board[x + i][y + i], EmptyField):
                valid.append((x, y, x + i, y + i))
            elif isinstance(self.board[x + i][y + i], Figure): 
                if self.board[x + i][y + i].color != self.board[x][y].color:
                    if isinstance(self.board[x + i][y + i], King):
                        self.check_moves[self.board[x + i][y + i].color].append((x, y, x + i, y + i))
                    else:
                        valid.append((x, y, x + i, y + i))
                else:
                   self.guarded_pieces[self.board[x][y].color].add((x + i, y + i)) 
                break
            else:
                break
        for i in range(1, min(x, y) + 1):
            if isinstance(self.board[x - i][y - i], EmptyField):
                valid.append((x, y, x - i, y - i))
            elif isinstance(self.board[x - i][y - i], Figure):
                if self.board[x - i][y - i].color != self.board[x][y].color:
                    if isinstance(self.board[x - i][y - i], King):
                        self.check_moves[self.board[x - i][y - i].color].append((x, y, x - i, y - i))
                    else:
                       valid.append((x, y, x - i, y - i))
                else:
                    self.guarded_pieces[self.board[x][y].color].add((x - i, y - i)) 
                break
            else:
                break
        for i in range(1, min(x, 8 - y)):
            if isinstance(self.board[x - i][y + i], EmptyField):
                valid.append((x, y, x - i, y + i))
            elif isinstance(self.board[x - i][y + i], Figure):
                if self.board[x - i][y + i].color != self.board[x][y].color:
                    if isinstance(self.board[x - i][y + i], King):
                        self.check_moves[self.board[x - i][y + i].color].append((x, y, x - i, y + i))
                    else:
                        valid.append((x, y, x - i, y + i))
                else:
                    self.guarded_pieces[self.board[x][y].color].add((x - i, y + i))
                break
            else:
                break
        for i in range(1, min(8 - x, y)):
            if isinstance(self.board[x + i][y - i], EmptyField):
                valid.append((x, y, x + i, y - i))
            elif isinstance(self.board[x + i][y - i], Figure):
                if self.board[x + i][y - i].color != self.board[x][y].color:
                    if isinstance(self.board[x + i][y - i], King):
                        self.check_moves[self.board[x + i][y - i].color].append((x, y, x + i, y - i))
                    else:
                        valid.append((x, y, x + i, y - i))
                else:
                    self.guarded_pieces[self.board[x][y].color].add((x + i, y - i))
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
                if isinstance(self.board[tmp_x][tmp_y], EmptyField):
                    valid.append((x, y, tmp_x, tmp_y))
                elif isinstance(self.board[tmp_x][tmp_y], Figure):
                    if self.board[tmp_x][tmp_y].color != self.board[x][y].color:
                        if isinstance(self.board[tmp_x][tmp_y], King):
                            self.check_moves[self.board[tmp_x][tmp_y].color].append((x, y, tmp_x, tmp_y))
                        else:
                            valid.append((x, y, tmp_x, tmp_y))
                    else:
                        self.guarded_pieces[self.board[x][y].color].add((tmp_x, tmp_y))
        if valid:
            return valid
    
    def get_king_valid_moves(self, x, y):
        valid = []
        for i in range(max(x - 1, 0), min(x + 2, 8)):
            for j in range(max(y - 1, 0), min(y + 2, 8)):
                if i == x and j == y:
                    self.is_check[self.board[x][y].color] = (len(self.check_moves[self.board[x][y].color]) != 0)
                elif isinstance(self.board[i][j], EmptyField) and not self.is_field_attacked(i, j, self.board[x][y].color):
                    valid.append((x, y, i, j))
                elif isinstance(self.board[i][j], Figure):
                    if self.board[i][j].color != self.board[x][y].color:
                        if (i, j) not in self.guarded_pieces[color((self.board[x][y].color.value + 1) % 2)]:
                            valid.append((x, y, i, j))
                    else:
                        self.guarded_pieces[self.board[x][y].color].add((i, j))
        if self.long_castle_valid(x, y):
            valid.append((x, y, i, j - 2))
        if self.short_castle_valid(x, y):
            valid.append((x, y, i, j + 2))
        if len(valid) == 0 and self.is_check[self.board[x][y].color]:
                self.checkmate[self.board[x][y].color] = True
        return valid
    
    def long_castle_valid(self, x, y):
        if self.long_castle_allowed:
            for i in range(1, y):
                if not isinstance(self.board[x][i], EmptyField) or self.is_field_attacked(x, i, self.board[x][y].color):
                    return False
        return True
    
    def short_castle_valid(self, x, y):
        if self.short_castle_allowed:
            for i in range(y + 1, 7):
                if not isinstance(self.board[x][i], EmptyField) or self.is_field_attacked(x, i, self.board[x][y].color):
                    return False
        return True

    def get_queen_valid_moves(self, x, y):
        valid = []
        valid.extend(self.get_rook_valid_moves(x, y))
        valid.extend(self.get_bishop_valid_moves(x, y))
        return valid
    
    def is_field_attacked(self, x, y, player_color):
        opposite_color = color((player_color.value + 1) % 2)
        if abs(x - self.kings_positions[opposite_color][0]) <= 1 and abs(y - self.kings_positions[opposite_color][1]) <= 1:
            return True
        for moves in self.valid_moves_by_color[opposite_color]:
            if moves:
                if moves[-2] == x and moves[-1] == y:
                    return True
        return False

    def simulate_move(self, old_x, old_y, new_x, new_y):
        piece = self.board[old_x][old_y]
        self.board[new_x][new_y] = self.board[old_x][old_y]
        self.board[old_x][old_y] = EmptyField()
        return piece

    def unmake_move(self, old_x, old_y, new_x, new_y, piece):
        self.board[old_x][old_y] = self.board[new_x][new_y]
        self.board[new_x][old_y] = piece

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

class EnPassantEmptyField(EmptyField):
    def __init__(self) -> None:
        super().__init__()

    def to_string(self):
        return super().to_string()

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
b.set_position('4k2r/8/8/8/3K4/8/8/R7 w - - 0 1')
b.print()

print('\n')




