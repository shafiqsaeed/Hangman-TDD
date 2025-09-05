"""Tkinter GUI for Hangman"""
import tkinter as tk
from tkinter import messagebox
import threading
import time
from hangman import Hangman

# Small default word list; replace or expand with a dictionary file if needed
WORDS = ["python", "test driven", "development", "hangman game", "openai", "hello world"]

class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game (TDD + GUI)")
        self.game = Hangman(WORDS)
        self.time_left = self.game.time_limit
        self.timer_running = False

        self.word_label = tk.Label(root, text=self.game.get_display_word(), font=("Courier", 24))
        self.word_label.pack(pady=20)

        self.entry = tk.Entry(root, font=("Arial", 16), width=5)
        self.entry.pack()
        self.entry.bind("<Return>", self.make_guess)

        self.timer_label = tk.Label(root, text=f"Time left: {self.time_left}s", font=("Arial", 14))
        self.timer_label.pack(pady=5)

        self.lives_label = tk.Label(root, text=f"Lives: {self.game.lives}", font=("Arial", 14))
        self.lives_label.pack(pady=5)

        self.guess_button = tk.Button(root, text="Guess", command=self.make_guess)
        self.guess_button.pack(pady=10)

        self.reset_button = tk.Button(root, text="Restart", command=self.restart_game)
        self.reset_button.pack(pady=5)

        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack(pady=5)

        self.start_timer()

    def make_guess(self, event=None):
        guess = self.entry.get().strip()
        if not guess:
            return
        accepted = self.game.guess(guess)
        # Update displays regardless; guess() will ignore invalid entries
        self.word_label.config(text=self.game.get_display_word())
        self.lives_label.config(text=f"Lives: {self.game.lives}")
        self.entry.delete(0, tk.END)

        if self.game.is_game_over():
            self.timer_running = False
            if self.game.did_win():
                messagebox.showinfo("Game Over", f"Congratulations! You won! The word was: {self.game.secret_word}")
            else:
                messagebox.showinfo("Game Over", f"You lost! The word was: {self.game.secret_word}")

    def start_timer(self):
        if self.timer_running:
            return
        self.timer_running = True
        self.time_left = self.game.time_limit

        def countdown():
            while self.timer_running and not self.game.is_game_over():
                if self.time_left > 0:
                    self.timer_label.config(text=f"Time left: {self.time_left}s")
                    time.sleep(1)
                    self.time_left -= 1
                else:
                    # timeout: deduct a life and reset timer
                    self.game.timeout()
                    self.lives_label.config(text=f"Lives: {self.game.lives}")
                    if self.game.is_game_over():
                        self.timer_running = False
                        messagebox.showinfo("Game Over", f"Time up! You lost! The word was: {self.game.secret_word}")
                        break
                    self.time_left = self.game.time_limit
        threading.Thread(target=countdown, daemon=True).start()

    def restart_game(self):
        self.game.reset_game()
        self.word_label.config(text=self.game.get_display_word())
        self.lives_label.config(text=f"Lives: {self.game.lives}")
        self.time_left = self.game.time_limit
        self.timer_label.config(text=f"Time left: {self.time_left}s")
        self.start_timer()

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()
