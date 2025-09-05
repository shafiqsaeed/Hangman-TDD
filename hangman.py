"""Core Hangman game logic + Console runner"""

import random
import string


class Hangman:
    """
    Core Hangman game logic (word/phrase version).
    This class is independent of any UI so it can be unit-tested.
    """

    def __init__(self, word_list=None, max_lives=6, time_limit=15):
        if word_list is None:
            # Default small dictionary (can be replaced with a full dictionary file)
            word_list = [
                "python",
                "java",
                "hangman",
                "programming",
                "developer",
                "hello world",
                "open source",
            ]
        self.word_list = word_list
        self.max_lives = max_lives
        self.time_limit = time_limit
        self.reset_game()

    def reset_game(self):
        self.secret_word = random.choice(self.word_list).lower()
        self.lives = self.max_lives
        self.guessed_letters = set()
        # display underscores for letters, keep non-alpha (like spaces) as-is
        self.display_word = ["_" if ch.isalpha() else ch for ch in self.secret_word]
        self.game_over = False
        self.won = False

    def guess(self, letter):
        """
        Process a guessed letter.
        Returns True if the guess was accepted (valid new letter), False otherwise.
        """
        if self.game_over:
            return False
        letter = letter.lower()
        if not letter.isalpha() or len(letter) != 1:
            return False
        if letter in self.guessed_letters:
            return False
        self.guessed_letters.add(letter)
        if letter in self.secret_word:
            for i, ch in enumerate(self.secret_word):
                if ch == letter:
                    self.display_word[i] = letter
            if "_" not in self.display_word:
                self.won = True
                self.game_over = True
        else:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
        return True

    def get_display_word(self):
        """Return the display word as a string (spaces between placeholders for readability)."""
        return " ".join(self.display_word)

    def timeout(self):
        """Called when timer expires for a guess."""
        if self.game_over:
            return
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True

    def is_game_over(self):
        return self.game_over

    def did_win(self):
        return self.won


# --------------------------
# Console Runner
# --------------------------
if __name__ == "__main__":
    words = [
        "python",
        "hangman",
        "test driven",
        "open source",
        "development",
        "hello world",
    ]
    game = Hangman(words, max_lives=6)

    print("🎮 Welcome to Hangman (Console Version)")
    print("Type a letter to guess. Type 'quit' to exit.\n")

    while not game.is_game_over():
        print(f"Word: {game.get_display_word()}")
        print(f"Lives left: {game.lives}")
        guess = input("Your guess: ").strip().lower()

        if guess == "quit":
            print("Thanks for playing!")
            break

        if not game.guess(guess):
            print("❌ Invalid or repeated guess.")

    if game.did_win():
        print(f"✅ You won! The word was: {game.secret_word}")
    elif not game.is_game_over():
        # this happens if player quit early
        print("👋 Game ended early.")
    else:
        print(f"💀 You lost! The word was: {game.secret_word}")
