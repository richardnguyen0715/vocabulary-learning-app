import tkinter as tk
from tkinter import ttk, messagebox
import random

class FlashcardWindow:
    def __init__(self, master, words, progress_model):
        self.master = master
        self.words = words
        self.progress_model = progress_model
        self.current_word = None
        self.show_answer = False
        
        self.master.title("Flashcards")
        self.master.geometry("600x400")
        self.master.resizable(False, False)
        
        self.create_widgets()
        self.next_card()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(fill='both', expand=True)

        # Card display area
        self.card_frame = ttk.Frame(main_frame)
        self.card_frame.pack(fill='both', expand=True, pady=20)

        self.card_text = tk.Text(self.card_frame, height=8, width=50, 
                                font=("Arial", 16), wrap=tk.WORD, 
                                state='disabled', cursor='arrow')
        self.card_text.pack(fill='both', expand=True)

        # Control buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=10)

        self.flip_btn = ttk.Button(btn_frame, text="Show Answer", command=self.flip_card)
        self.flip_btn.pack(side='left', padx=5)

        self.correct_btn = ttk.Button(btn_frame, text="Correct", command=self.mark_correct, state='disabled')
        self.correct_btn.pack(side='left', padx=5)

        self.incorrect_btn = ttk.Button(btn_frame, text="Incorrect", command=self.mark_incorrect, state='disabled')
        self.incorrect_btn.pack(side='left', padx=5)

        self.next_btn = ttk.Button(btn_frame, text="Next Card", command=self.next_card)
        self.next_btn.pack(side='right', padx=5)

        # Progress info
        self.progress_label = ttk.Label(main_frame, text="")
        self.progress_label.pack(pady=5)

    def next_card(self):
        if not self.words:
            messagebox.showinfo("Info", "No more words!")
            self.master.destroy()
            return

        self.current_word = random.choice(self.words)
        self.show_answer = False
        self.update_card_display()
        self.flip_btn.config(text="Show Answer")
        self.correct_btn.config(state='disabled')
        self.incorrect_btn.config(state='disabled')

    def flip_card(self):
        self.show_answer = not self.show_answer
        self.update_card_display()
        
        if self.show_answer:
            self.flip_btn.config(text="Show Question")
            self.correct_btn.config(state='normal')
            self.incorrect_btn.config(state='normal')
        else:
            self.flip_btn.config(text="Show Answer")
            self.correct_btn.config(state='disabled')
            self.incorrect_btn.config(state='disabled')

    def update_card_display(self):
        self.card_text.config(state='normal')
        self.card_text.delete(1.0, tk.END)
        
        if not self.show_answer:
            # Show English word and ask for meaning
            content = f"Word: {self.current_word['word'].upper()}\n\n"
            if self.current_word.get('pronunciation'):
                content += f"Pronunciation: {self.current_word['pronunciation']}\n\n"
            if self.current_word.get('part_of_speech'):
                content += f"Part of Speech: {self.current_word['part_of_speech']}\n\n"
            content += "What does this word mean in Vietnamese?"
        else:
            # Show the answer
            content = f"Word: {self.current_word['word'].upper()}\n\n"
            content += f"Vietnamese: {self.current_word['vietnamese_meaning']}\n\n"
            if self.current_word.get('english_meaning'):
                content += f"English: {self.current_word['english_meaning']}\n\n"
            if self.current_word.get('example'):
                content += f"Example: {self.current_word['example']}"

        self.card_text.insert(1.0, content)
        self.card_text.config(state='disabled')

    def mark_correct(self):
        if self.progress_model and self.current_word:
            self.progress_model.update_progress(str(self.current_word['_id']), True)
        self.next_card()

    def mark_incorrect(self):
        if self.progress_model and self.current_word:
            self.progress_model.update_progress(str(self.current_word['_id']), False)
        self.next_card()