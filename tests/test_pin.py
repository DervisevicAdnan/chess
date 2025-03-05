from engine import Board, color

class Test_pin:
    def test_pin_1(self):
        # Pins
        b = Board()
        b.set_position('rnbqk1nr/ppp2ppp/8/3p3Q/1b1P1p2/2P1P3/PP3PPP/RN2KBNR b KQkq - 1 5')   
        assert b.pinned_moves[color.BLACK] == [(3, 7, 2, 6), (3, 7, 1, 5)]
        assert b.pinned_moves[color.WHITE] == [(4, 1, 5, 2), (4, 1, 6, 3)]