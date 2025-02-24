import tkinter as tk
import random
import sqlite3

# List of words
WORDS = ["python", "hangman", "developer", "tkinter", "database"]

# Database setup
def setup_database():
    conn = sqlite3.connect("hangman_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT,
            attempts INTEGER,
            result TEXT
        )
    """)
    conn.commit()
    conn.close()

setup_database()

# Hangman Game Class
class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        
        self.word = random.choice(WORDS)
        self.display_word = ["_" for _ in self.word]
        self.attempts = 6
        self.guessed_letters = set()
        
        self.label_word = tk.Label(root, text=" ".join(self.display_word), font=("Arial", 18))
        self.label_word.pack(pady=10)
        
        self.label_attempts = tk.Label(root, text=f"Attempts Left: {self.attempts}", font=("Arial", 14))
        self.label_attempts.pack(pady=5)
        
        self.entry_guess = tk.Entry(root, font=("Arial", 14))
        self.entry_guess.pack(pady=5)
        
        self.button_guess = tk.Button(root, text="Guess", command=self.make_guess)
        self.button_guess.pack(pady=5)
        
        self.label_result = tk.Label(root, text="", font=("Arial", 14))
        self.label_result.pack(pady=10)
        
        self.button_restart = tk.Button(root, text="Restart", command=self.restart_game)
        self.button_restart.pack(pady=5)
    
    def make_guess(self):
        letter = self.entry_guess.get().lower()
        self.entry_guess.delete(0, tk.END)
        
        if not letter.isalpha() or len(letter) != 1 or letter in self.guessed_letters:
            return
        
        self.guessed_letters.add(letter)
        
        if letter in self.word:
            for i, char in enumerate(self.word):
                if char == letter:
                    self.display_word[i] = letter
        else:
            self.attempts -= 1
        
        self.update_display()
        self.check_game_over()
    
    def update_display(self):
        self.label_word.config(text=" ".join(self.display_word))
        self.label_attempts.config(text=f"Attempts Left: {self.attempts}")
    
    def check_game_over(self):
        if "_" not in self.display_word:
            self.save_game_result("Won")
            self.label_result.config(text="You Won!", fg="green")
            self.button_guess.config(state=tk.DISABLED)
        elif self.attempts == 0:
            self.save_game_result("Lost")
            self.label_result.config(text=f"You Lost! The word was '{self.word}'", fg="red")
            self.button_guess.config(state=tk.DISABLED)
    
    def save_game_result(self, result):
        conn = sqlite3.connect("hangman_history.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO game_history (word, attempts, result) VALUES (?, ?, ?)", (self.word, self.attempts, result))
        conn.commit()
        conn.close()
    
    def restart_game(self):
        self.word = random.choice(WORDS)
        self.display_word = ["_" for _ in self.word]
        self.attempts = 6
        self.guessed_letters.clear()
        self.label_result.config(text="")
        self.button_guess.config(state=tk.NORMAL)
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()