import unittest
import blackjack

class TestDeck(unittest.TestCase):
    def testDeckInit(self):
        d = blackjack.Deck()
        self.assertEqual(len(d.cards),52)
        self.assertEqual(len(set(d.cards)), 52)
    
    def testDeckShuffle(self):
        d = blackjack.Deck()
        d.shuffle()
        self.assertEqual(len(d.cards), 52)
        self.assertEqual(len(set(d.cards)), 52)

class TestCard(unittest.TestCase):
    def testCardValue(self):
        c = blackjack.Card("Hearts", "Ace")
        self.assertEqual(c.value(), 11)

class TestHand(unittest.TestCase):
    def testHandTotal(self):
        h = blackjack.Hand()
        h.add_card(blackjack.Card("Hearts", "Ace"))
        self.assertEqual(h.total, 11)
        h.add_card(blackjack.Card("Club", "Ace"))
        self.assertEqual(h.total, 12)
    
if __name__ == '__main__':
    unittest.main()