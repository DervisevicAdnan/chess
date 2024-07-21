from engine import Board

class TestDraw:
    def test_one(self):
        # Stalemate - pjesaci blokiraju 
        b = Board()
        b.set_position('8/8/8/8/3k4/2ppp3/3p4/3K4 w - - 0 1')
        assert b.draw == True
    
    def test_two(self):
        # Stalemate - topovi i kralj blokiraju
        b = Board()
        b.set_position('1R6/8/8/8/p2R4/k7/8/1K6 b - - 0 99')
        assert b.draw == True

    def test_three(self):
        # Stalemate - lovac i pjesaci blokiraju
        b = Board()
        b.set_position('6k1/b7/8/8/5p2/7p/7P/7K w - - 0 54')
        assert b.draw == True

    def test_four(self):
        # Stalemate - dama blokira
        b = Board()
        b.set_position('8/8/8/8/8/8/3K1Q2/7k b - - 0 1')
        assert b.draw == True
    
    def test_five(self):
        # Stalemate - skakaci blokiraju
        b = Board()
        b.set_position('8/8/8/8/6b1/5knn/7K/8 w - - 0 1')
        assert b.draw == True

    def test_six(self):
        # Insufficient material - Kralj v kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/K1k5 w - - 0 1')
        assert b.draw == True

    def test_seven(self):
        # Insufficient material - Bijeli kralj & bijeli lovac v crni kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/K1kB4 w - - 0 1')
        assert b.draw == True 

    def test_eigth(self):
        # Insufficient material - Crni kralj & crni lovac v bijeli kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/k1Kb4 w - - 0 1')
        assert b.draw == True 

    def test_nine(self):
        # Insufficient material - Bijeli kralj & bijeli skakac v crni kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/K1kN4 w - - 0 1')
        assert b.draw == True 

    def test_ten(self):
        # Insufficient material - Crni kralj & crni skakac v bijeli kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/k1Kn4 w - - 0 1')
        assert b.draw == True 

    def test_eleven(self):
        # Insufficient material - Kraljevi i lovci, lovci na polju iste (crne) boje
        b = Board()
        b.set_position('8/8/8/8/8/8/8/k1b1K1B1 w - - 0 1')
        assert b.draw == True 

    def test_twelve(self):
        # Insufficient material - Kraljevi i lovci, lovci na polju iste (bijele) boje
        b = Board()
        b.set_position('8/8/8/8/8/8/8/kb2K2B w - - 0 1')
        assert b.draw == True 

    def test_thirteen(self):
        # Insufficient material - Crni kralj i crni lovac na bijelom polju v bijeli kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/kb2K3 w - - 0 1')
        assert b.draw == True 

    def test_fourteen(self):
        # Insufficient material - Crni kralj i crni lovac na crnom polju v bijeli kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/1b6/k3K3 w - - 0 1')
        assert b.draw == True 

    def test_fifteen(self):
        # Insufficient material - Bijeli kralj i bijeli lovac na crnom polju v crni kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/k3K1B1 w - - 0 1')
        assert b.draw == True 

    def test_sixteen(self):
        # Insufficient material - Bijeli kralj i bijeli lovac na bijelom polju v crni kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/k3KB2 w - - 0 1')
        assert b.draw == True    