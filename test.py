from engine import Board, color

class TestDraw:
    def test_1(self):
        # Stalemate - pjesaci blokiraju 
        b = Board()
        b.set_position('8/8/8/8/3k4/2ppp3/3p4/3K4 w - - 0 1')
        assert b.draw == True
    
    def test_2(self):
        # Stalemate - topovi i kralj blokiraju
        b = Board()
        b.set_position('1R6/8/8/8/p2R4/k7/8/1K6 b - - 0 99')
        assert b.draw == True

    def test_3(self):
        # Stalemate - lovac i pjesaci blokiraju
        b = Board()
        b.set_position('6k1/b7/8/8/5p2/7p/7P/7K w - - 0 54')
        assert b.draw == True

    def test_4(self):
        # Stalemate - dama blokira
        b = Board()
        b.set_position('8/8/8/8/8/8/3K1Q2/7k b - - 0 1')
        assert b.draw == True
    
    def test_5(self):
        # Stalemate - skakaci blokiraju
        b = Board()
        b.set_position('8/8/8/8/6b1/5knn/7K/8 w - - 0 1')
        assert b.draw == True

    def test_6(self):
        # Insufficient material - Kralj v kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/K1k5 w - - 0 1')
        assert b.draw == True

    def test_7(self):
        # Insufficient material - Bijeli kralj & bijeli lovac v crni kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/K1kB4 w - - 0 1')
        assert b.draw == True 

    def test_8(self):
        # Insufficient material - Crni kralj & crni lovac v bijeli kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/k1Kb4 w - - 0 1')
        assert b.draw == True 

    def test_9(self):
        # Insufficient material - Bijeli kralj & bijeli skakac v crni kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/K1kN4 w - - 0 1')
        assert b.draw == True 

    def test_10(self):
        # Insufficient material - Crni kralj & crni skakac v bijeli kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/k1Kn4 w - - 0 1')
        assert b.draw == True 

    def test_11(self):
        # Insufficient material - Kraljevi i lovci, lovci na polju iste (crne) boje
        b = Board()
        b.set_position('8/8/8/8/8/8/8/k1b1K1B1 w - - 0 1')
        assert b.draw == True 

    def test_12(self):
        # Insufficient material - Kraljevi i lovci, lovci na polju iste (bijele) boje
        b = Board()
        b.set_position('8/8/8/8/8/8/8/kb2K2B w - - 0 1')
        assert b.draw == True 

    def test_13(self):
        # Insufficient material - Crni kralj i crni lovac na bijelom polju v bijeli kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/kb2K3 w - - 0 1')
        assert b.draw == True 

    def test_14(self):
        # Insufficient material - Crni kralj i crni lovac na crnom polju v bijeli kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/1b6/k3K3 w - - 0 1')
        assert b.draw == True 

    def test_15(self):
        # Insufficient material - Bijeli kralj i bijeli lovac na crnom polju v crni kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/k3K1B1 w - - 0 1')
        assert b.draw == True 

    def test_16(self):
        # Insufficient material - Bijeli kralj i bijeli lovac na bijelom polju v crni kralj
        b = Board()
        b.set_position('8/8/8/8/8/8/8/k3KB2 w - - 0 1')
        assert b.draw == True 

    def test_17(self):
        # Half moves
        b = Board()
        b.set_position('8/8/8/4k2p/7P/4K3/8/8 w - - 100 200')   
        assert b.draw == True

    def test_18(self):
        # Pins
        b = Board()
        b.set_position('rnbqk1nr/ppp2ppp/8/3p3Q/1b1P1p2/2P1P3/PP3PPP/RN2KBNR b KQkq - 1 5')   
        assert b.pinned_moves[color.BLACK] == [(3, 7, 2, 6), (3, 7, 1, 5)]
        assert b.pinned_moves[color.WHITE] == [(4, 1, 5, 2), (4, 1, 6, 3)]

    def test_19(self):
        # Pins
        b = Board()
        b.set_position('rnbqk1nr/ppp2ppp/8/3pp2Q/1bPP4/4P3/PP3PPP/RN2KBNR b KQkq - 1 5')
        # manuelno podesujemo is_check za bijelog dok ne popravimo
        b.is_check[color.WHITE] = True
        b.update_valid_moves()
        assert b.valid_moves_by_color[color.WHITE] == [(7, 1, 5, 2), (7, 1, 6, 3)] 

    def test_20(self):
        b = Board()
        b.set_position('rnbqk1nr/ppp2ppp/8/3pp2Q/1bPP4/4P3/PP3PPP/RN2KBNR b KQkq - 1 5')
        assert b.valid_moves_by_color[color.WHITE] == [(3, 7, 4, 7), (3, 7, 5, 7), (3, 7, 2, 7), (3, 7, 1, 7), (3, 7, 3, 6), (3, 7, 3, 5), (3, 7, 3, 4), (3, 7, 2, 6), (3, 7, 1, 5), (3, 7, 4, 6), (3, 7, 5, 5), (3, 7, 6, 4), (3, 7, 7, 3), (7, 1, 5, 0), (7, 1, 5, 2), (7, 1, 6, 3), (7, 5, 6, 4), (7, 5, 5, 3), (7, 6, 5, 5), (7, 6, 5, 7), (7, 6, 6, 4)] 