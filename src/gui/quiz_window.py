import tkinter as tk
from tkinter import ttk, messagebox
import random

class QuizWindow:
    def __init__(self, master, words, progress_model):
        self.master = master
        self.words = words
        self.progress_model = progress_model
        self.current_question = 0
        self.score = 0
        self.quiz_words = []
        self.quiz_type = "multiple_choice"
        
        self.master.title("Vocabulary Quiz")
        self.master.geometry("600x500")
        self.master.resizable(False, False)
        
        self.setup_quiz()
        self.create_widgets()
        self.show_question()

    def setup_quiz(self):
        # Select random words for quiz (max 10)
        self.quiz_words = random.sample(self.words, min(10, len(self.words)))
        random.shuffle(self.quiz_words)

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(fill='both', expand=True)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 20))

        ttk.Label(header_frame, text="Vocabulary Quiz", 
                 font=("Arial", 18, "bold")).pack()

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(header_frame, variable=self.progress_var, 
                                          maximum=len(self.quiz_words))
        self.progress_bar.pack(fill='x', pady=10)

        # Question info
        self.question_info = ttk.Label(header_frame, text="", font=("Arial", 12))
        self.question_info.pack()

        # Question frame
        self.question_frame = ttk.LabelFrame(main_frame, text="Question", padding="15")
        self.question_frame.pack(fill='both', expand=True, pady=10)

        self.question_label = ttk.Label(self.question_frame, text="", 
                                       font=("Arial", 14), wraplength=500)
        self.question_label.pack(pady=20)

        # Answer frame
        self.answer_frame = ttk.Frame(self.question_frame)
        self.answer_frame.pack(fill='x', pady=10)

        # Multiple choice options
        self.answer_var = tk.StringVar()
        self.option_buttons = []
        for i in range(4):
            btn = ttk.Radiobutton(self.answer_frame, text="", variable=self.answer_var, 
                                 value=str(i), font=("Arial", 12))
            btn.pack(anchor='w', pady=5)
            self.option_buttons.append(btn)

        # Text entry for fill-in-the-blank
        self.answer_entry = ttk.Entry(self.answer_frame, font=("Arial", 12), width=30)
        
        # Control buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=20)

        self.submit_btn = ttk.Button(btn_frame, text="Submit Answer", command=self.submit_answer)
        self.submit_btn.pack(side='left', padx=5)

        self.next_btn = ttk.Button(btn_frame, text="Next Question", command=self.next_question, 
                                  state='disabled')
        self.next_btn.pack(side='left', padx=5)

        # Quiz type selector
        type_frame = ttk.Frame(btn_frame)
        type_frame.pack(side='right')

        ttk.Label(type_frame, text="Quiz Type:").pack(side='left', padx=5)
        self.type_var = tk.StringVar(value="multiple_choice")
        type_combo = ttk.Combobox(type_frame, textvariable=self.type_var, 
                                 values=["multiple_choice", "fill_blank"], 
                                 state="readonly", width=15)
        type_combo.pack(side='left')
        type_combo.bind('<<ComboboxSelected>>', self.change_quiz_type)

    def change_quiz_type(self, event):
        self.quiz_type = self.type_var.get()
        self.show_question()

    def show_question(self):
        if self.current_question >= len(self.quiz_words):
            self.show_results()
            return

        word = self.quiz_words[self.current_question]
        
        # Update progress
        self.progress_var.set(self.current_question)
        self.question_info.config(text=f"Question {self.current_question + 1} of {len(self.quiz_words)}")

        if self.quiz_type == "multiple_choice":
            self.show_multiple_choice(word)
        else:
            self.show_fill_blank(word)

        # Reset buttons
        self.submit_btn.config(state='normal')
        self.next_btn.config(state='disabled')

    def show_multiple_choice(self, word):
        # Hide text entry
        self.answer_entry.pack_forget()
        
        # Show radio buttons
        for btn in self.option_buttons:
            btn.pack(anchor='w', pady=5)

        # Set question
        question_text = f"What is the Vietnamese meaning of '{word['word']}'?"
        if word.get('pronunciation'):
            question_text += f"\nPronunciation: {word['pronunciation']}"
        
        self.question_label.config(text=question_text)

        # Generate options
        correct_answer = word['vietnamese_meaning']
        wrong_answers = []
        
        # Get other words for wrong answers
        other_words = [w for w in self.words if w['_id'] != word['_id']]
        random.shuffle(other_words)
        
        for other_word in other_words:
            if len(wrong_answers) < 3:
                wrong_answers.append(other_word['vietnamese_meaning'])

        # Fill remaining slots if needed
        while len(wrong_answers) < 3:
            wrong_answers.append(f"Wrong answer {len(wrong_answers) + 1}")

        # Mix correct and wrong answers
        all_options = [correct_answer] + wrong_answers
        random.shuffle(all_options)

        # Set options to buttons
        self.correct_option = str(all_options.index(correct_answer))
        for i, option in enumerate(all_options):
            self.option_buttons[i].config(text=option)

        self.answer_var.set("")

    def show_fill_blank(self, word):
        # Hide radio buttons
        for btn in self.option_buttons:
            btn.pack_forget()
        
        # Show text entry
        self.answer_entry.pack(pady=10)
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()

        # Set question
        question_text = f"Enter the Vietnamese meaning of '{word['word']}':"
        if word.get('pronunciation'):
            question_text += f"\nPronunciation: {word['pronunciation']}"
        
        self.question_label.config(text=question_text)

    def submit_answer(self):
        word = self.quiz_words[self.current_question]
        is_correct = False

        if self.quiz_type == "multiple_choice":
            selected = self.answer_var.get()
            is_correct = selected == self.correct_option
        else:  # fill_blank
            user_answer = self.answer_entry.get().strip().lower()
            correct_answer = word['vietnamese_meaning'].lower()
            is_correct = user_answer == correct_answer

        # Update score
        if is_correct:
            self.score += 1
            messagebox.showinfo("Correct!", "That's the right answer!")
        else:
            correct_meaning = word['vietnamese_meaning']
            messagebox.showinfo("Incorrect", f"The correct answer is: {correct_meaning}")

        # Update progress in database
        if self.progress_model:
            self.progress_model.update_progress(str(word['_id']), is_correct)

        # Enable next button
        self.submit_btn.config(state='disabled')
        self.next_btn.config(state='normal')

    def next_question(self):
        self.current_question += 1
        self.show_question()

    def show_results(self):
        # Update progress bar
        self.progress_var.set(len(self.quiz_words))
        
        # Clear question area
        self.question_label.config(text="Quiz Complete!")
        for btn in self.option_buttons:
            btn.pack_forget()
        self.answer_entry.pack_forget()

        # Show results
        percentage = (self.score / len(self.quiz_words)) * 100
        result_text = f"Your Score: {self.score}/{len(self.quiz_words)} ({percentage:.1f}%)\n\n"
        
        if percentage >= 80:
            result_text += "Excellent work! 🎉"
        elif percentage >= 60:
            result_text += "Good job! Keep practicing! 👍"
        else:
            result_text += "Keep studying! You'll improve! 📚"

        result_label = ttk.Label(self.answer_frame, text=result_text, 
                               font=("Arial", 14), justify='center')
        result_label.pack(pady=20)

        # Hide control buttons and show close button
        self.submit_btn.pack_forget()
        self.next_btn.pack_forget()
        
        close_btn = ttk.Button(self.answer_frame, text="Close Quiz", 
                              command=self.master.destroy)
        close_btn.pack(pady=10)