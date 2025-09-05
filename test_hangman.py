"""Unit tests for Hangman game using unittest"""
import unittest
from hangman import Hangman

class TestHangman(unittest.TestCase):

    def setUp(self):
        self.words = ["python", "hangman"]
        self.game = Hangman(self.words, max_lives=3)

    def test_initial_state(self):
        self.assertEqual(self.game.lives, 3)
        self.assertIn("_", self.game.get_display_word())

    def test_correct_guess(self):
        self.game.secret_word = "python"
        self.game.display_word = ["_"] * len("python")
        accepted = self.game.guess("p")
        self.assertTrue(accepted)
        self.assertIn("p", self.game.get_display_word())

    def test_incorrect_guess(self):
        self.game.secret_word = "python"
        self.game.display_word = ["_"] * len("python")
        self.game.guess("z")
        self.assertEqual(self.game.lives, 2)

    def test_win_condition(self):
        self.game.secret_word = "hi"
        self.game.display_word = ["_"] * 2
        self.game.guess("h")
        self.game.guess("i")
        self.assertTrue(self.game.did_win())
        self.assertTrue(self.game.is_game_over())

    def test_loss_condition(self):
        self.game.secret_word = "hi"
        self.game.display_word = ["_"] * 2
        self.game.guess("z")
        self.game.guess("y")
        self.game.guess("x")
        self.assertFalse(self.game.did_win())
        self.assertTrue(self.game.is_game_over())

if __name__ == "__main__":
    unittest.main()
