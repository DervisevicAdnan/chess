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

        self.pinned_moves = { color.BLACK: [], color.WHITE: []}

        starting_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.board = []
        self.set_position(starting_FEN)
        self.update_valid_moves()

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

        # Stavljeno da se ne postavlja slucaj kada pise samo -
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

        self.half_moves = int(split[4])

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
        self.update_valid_moves()

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
        self.pinned_moves = { color.BLACK: [], color.WHITE: []}
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
        if self.half_moves == 100:
            self.draw = True
        if self.is_insufficient_material(self.encode_FEN()):
            self.draw = True
        self.filter_pinned_figure_moves()
        

        
    def is_insufficient_material(self, FEN):
        position = FEN.split()[0]
        remaining_pieces = position.replace('/', '')

        piece_count = {
            'r': 0,
            'n': 0,
            'b': 0,
            'q': 0,
            'k': 0,
            'p': 0,
            'R': 0,
            'N': 0,
            'B': 0,
            'Q': 0,
            'K': 0,
            'P': 0
        }

        for character in remaining_pieces:
            if character.isalpha():
                piece_count[character] += 1

        if piece_count['r'] == 0 and piece_count['q'] == 0 and piece_count['p'] == 0 and piece_count['R'] == 0 and piece_count['Q'] == 0 and piece_count['P'] == 0:
            if piece_count['b'] == 0 and piece_count['B'] == 0:
                if piece_count['n'] == 0 and piece_count['N'] == 0:
                    return True
                if (piece_count['n'] == 1 and piece_count['N'] == 0) or (piece_count['n'] == 0 and piece_count['N'] == 1):
                    return True
            if piece_count['n'] == 0 and piece_count['N'] == 0:
                if (piece_count['b'] == 1 and piece_count['B'] == 0) or (piece_count['b'] == 0 and piece_count['B'] == 1):
                    return True
                elif piece_count['b'] == 1 and piece_count['B'] == 1:
                    bishops = [i for i, char in enumerate(remaining_pieces) if char in 'bB']
                    same_color = all((i // 8 + i % 8) % 2 == 0 for i in bishops) or all((i // 8 + i % 8) % 2 == 1 for i in bishops)
                    if same_color:
                        return True

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
        # x <, x + , x ==, enpassant x ==
        move_data = [7, 1, 1, 4]
        if self.board[x][y].color == color.WHITE:
            move_data = [0, -1, 6, 3]
        valid = []

        if x < move_data[0]:
            tmp_x = x + move_data[1]
            if isinstance(self.board[tmp_x][y], EmptyField):
                valid.append((x, y, tmp_x, y))
                if x == move_data[2] and isinstance(self.board[tmp_x + move_data[1]][y], EmptyField):
                    valid.append((x, y, tmp_x + move_data[1], y))
            if y < 7 and isinstance(self.board[tmp_x][y + 1], Figure):
                if self.board[tmp_x][y + 1].color != self.board[x][y].color:
                    if isinstance(self.board[tmp_x][y + 1], King):
                        self.check_moves[self.board[tmp_x][y + 1].color].append((x, y, tmp_x, y + 1))
                    else:
                        valid.append((x, y, tmp_x, y + 1))
                else:
                    self.guarded_pieces[self.board[x][y].color].add((tmp_x, y + 1))
            if y > 0 and isinstance(self.board[tmp_x][y - 1], Figure):
                if self.board[tmp_x][y - 1].color != self.board[x][y].color:
                    if isinstance(self.board[tmp_x][y - 1], King):
                        self.check_moves[self.board[tmp_x][y - 1].color].append((x, y, tmp_x, y - 1))
                    else:
                        valid.append((x, y, tmp_x, y - 1))
                else:
                    self.guarded_pieces[self.board[x][y].color].add((tmp_x, y - 1))
            if x == move_data[3]:
                if y < 7 and isinstance(self.board[tmp_x][y + 1], EnPassantEmptyField):
                    valid.append((x, y, tmp_x, y + 1))
                if y > 0 and isinstance(self.board[tmp_x][y - 1], EnPassantEmptyField):
                    valid.append((x, y, tmp_x, y - 1))
        return valid

    def get_rook_valid_moves(self, x, y):
        loop_ranges = [[(x + 1, 8), (y, y + 1)], [(x - 1, -1, -1), (y, y + 1)], [(x, x + 1), (y + 1, 8)], [(x, x + 1), (y - 1, -1, -1)]]
        valid = []
        for loop_range in loop_ranges:
            break_flag = False
            pinned = []
            ignore_for_valid = False
            for i in range(*loop_range[0]):
                for j in range(*loop_range[1]):
                    if isinstance(self.board[i][j], EmptyField):
                        if not ignore_for_valid:
                            valid.append((x, y, i, j))
                        pinned.append((x, y, i, j))
                    elif isinstance(self.board[i][j], Figure):
                        if self.board[i][j].color != self.board[x][y].color:
                            if isinstance(self.board[i][j], King):
                                self.check_moves[self.board[i][j].color].append((x, y, i, j))
                                self.pinned_moves[self.board[i][j].color].extend(pinned)
                                break
                            else:
                                if not ignore_for_valid:
                                    valid.append((x, y, i, j))
                                    pinned.append((x, y, i, j))
                                    ignore_for_valid = True
                                else:
                                    break_flag = True
                                    break
                        else:
                            self.guarded_pieces[self.board[x][y].color].add((i, j))
                            break_flag = True
                            break
                    else:
                        break_flag = True
                        break
                if break_flag:
                    break
        return valid
    
    def get_bishop_valid_moves(self, x, y):
        loop_ranges = [[(1, min(8 - x, 8 - y)), 1, 1], [(1, min(x, y) + 1), -1, -1], [(1, min(x + 1, 8 - y)), -1, 1], [(1, min(8 - x, y + 1)), 1, -1]]
        valid = []
        for loop_range in loop_ranges:
            ignore_for_valid = False
            pinned = []
            for i in range(*loop_range[0]):
                tmp_x = loop_range[1] * i + x
                tmp_y = loop_range[2] * i + y
                if isinstance(self.board[tmp_x][tmp_y], EmptyField):
                    if not ignore_for_valid:
                        valid.append((x, y, tmp_x, tmp_y))
                    pinned.append((x, y, tmp_x, tmp_y))
                elif isinstance(self.board[tmp_x][tmp_y], Figure): 
                    if self.board[tmp_x][tmp_y].color != self.board[x][y].color:
                        if isinstance(self.board[tmp_x][tmp_y], King):
                            self.check_moves[self.board[tmp_x][tmp_y].color].append((x, y, tmp_x, tmp_y))
                            self.pinned_moves[self.board[tmp_x][tmp_y].color].extend(pinned)
                            break
                        else:
                            if not ignore_for_valid:
                                valid.append((x, y, tmp_x, tmp_y))
                                pinned.append((x, y, tmp_x, tmp_y))
                                ignore_for_valid = True
                            else:
                                break
                    else:
                        self.guarded_pieces[self.board[x][y].color].add((tmp_x, tmp_y)) 
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
                        if (i, j) not in self.guarded_pieces[color((self.board[x][y].color.value + 1) % 2)] and not self.is_field_attacked(i, j, self.board[x][y].color):
                            valid.append((x, y, i, j))
                    else:
                        self.guarded_pieces[self.board[x][y].color].add((i, j))
        if self.long_castle_valid(x, y):
            valid.append((x, y, x, y - 2))
        if self.short_castle_valid(x, y):
            valid.append((x, y, x, y + 2))
        # ne mozemo ovdje checkmate provjeravati, bar ne ovako
        if len(valid) == 0 and self.is_check[self.board[x][y].color]:
                self.checkmate[self.board[x][y].color] = True
        return valid
    
    def long_castle_valid(self, x, y):
        if not self.long_castle_allowed[self.board[x][y].color]:
            return False
        for i in range(1, y):
            if not isinstance(self.board[x][i], EmptyField) or self.is_field_attacked(x, i, self.board[x][y].color):
                return False
        return True
    
    def short_castle_valid(self, x, y):
        if not self.short_castle_allowed[self.board[x][y].color]:
            return False
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

        pawn_moves = [(-1, -1), (-1, 1)] if player_color == color.WHITE else [(1, -1), (1, 1)]

        for X, Y in pawn_moves:
            if 0 <= X + x < 8 and 0 <= Y + y < 8 and isinstance(self.board[x + X][y + Y], Pawn) and self.board[x + X][y + Y].color == opposite_color:
                return True

        for moves in self.valid_moves_by_color[opposite_color]:
            if moves:
                if moves[-2] == x and moves[-1] == y:
                    return True
        return False
    
    def filter_pinned_figure_moves(self):
        #print("-"*20)
        #print("Pinovanje\n")
        for clr in color:
            #print(clr)
            for move in self.valid_moves_by_color[clr]:
                pinovani = [pin_field for pin_field in self.pinned_moves[clr] if pin_field[-2:] == move[:2]]
                #print(pinovani)
                
                if len(pinovani) == 1:
                    i = 0
                    while i < len(self.valid_moves_by_color[clr]):
                        #print("Indeks ", i)
                        mv = self.valid_moves_by_color[clr][i]
                        if move[:2] == mv[:2]:
                            #print("Unutrasnja provjera za ", mv)
                            #print([pin for pin in self.pinned_moves[clr] if mv[-2:] == pin[-2:] and pin[:2] == pinovani[0][:2]])
                            pin_polje = any(pin for pin in self.pinned_moves[clr] if mv[-2:] == pin[-2:] and pin[:2] == pinovani[0][:2])
                            if not (pin_polje or mv[-2:] == pinovani[0][:2]):
                                self.valid_moves_by_color[clr].remove(mv)
                                i -= 1
                        i += 1
                


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
#b.set_position('rnb1kbnr/ppp2q1p/8/7Q/4P3/8/PPP2PPP/RNB1KBNR w KQkq - 0 1')
b.set_position('rnb1kbnr/ppp2q1p/8/4Q3/4P3/8/PPP2PPP/RNB1KBNR w KQkq - 0 1')
#b.set_position("rnbqk1nr/ppp2ppp/8/3pp2Q/1bPP4/4P3/PP3PPP/RN2KBNR b KQkq - 1 5")
b.print()

print('\n')

print("Check for black?")
print(b.is_check[color.BLACK])

#b.update_valid_moves()
print(len(b.valid_moves_by_color[color.WHITE]))

print("Pinned black: ", b.pinned_moves[color.BLACK], "\n")

print("Pinned white: ", b.pinned_moves[color.WHITE], "\n")

print("potezi crni: ", b.valid_moves_by_color[color.BLACK], "\n")
print("potezi bijeli: ", b.valid_moves_by_color[color.WHITE], "\n")