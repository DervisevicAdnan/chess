from enum import Enum

class color(Enum):
    WHITE = 1
    BLACK = 2

class Board:

    '''
    
    board 
    
    bR bN bB bQ bK bB bN bR
    bP bP bP bP bP bP bP bP



    
    wP wP wP wP wP wP wP wP
    wR wN wB wQ wK wB wN wR

    '''

    def __init__(self):
        self.set_starting_order()
        for i in range(8):
            row = []
            for j in range(8):
                row.append(Field)
            self.board.append(row)

    def set_starting_order(self):
        self.board = [[Rook(color.BLACK),Knight(color.BLACK),Bishop(color.BLACK),Queen(color.BLACK),King(color.BLACK),Bishop(color.BLACK),Knight(color.BLACK),Rook(color.BLACK)],
                      [Pawn(color.BLACK), Pawn(color.BLACK), Pawn(color.BLACK), Pawn(color.BLACK), Pawn(color.BLACK), Pawn(color.BLACK), Pawn(color.BLACK), Pawn(color.BLACK)],
                      [EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField()],
                      [EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField()],
                      [EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField()],
                      [EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField(), EmptyField()],
                      [Pawn(color.WHITE), Pawn(color.WHITE), Pawn(color.WHITE), Pawn(color.WHITE), Pawn(color.WHITE), Pawn(color.WHITE), Pawn(color.WHITE), Pawn(color.WHITE)],
                      [Rook(color.WHITE),Knight(color.WHITE),Bishop(color.WHITE),Queen(color.WHITE),King(color.WHITE),Bishop(color.WHITE),Knight(color.WHITE),Rook(color.WHITE)]]
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