import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class ProgressWindow:
    def __init__(self, master, progress_model, vocab_model):
        self.master = master
        self.progress_model = progress_model
        self.vocab_model = vocab_model
        
        self.master.title("Learning Progress")
        self.master.geometry("700x500")
        self.master.resizable(True, True)
        
        self.create_widgets()
        self.load_progress_data()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill='both', expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Learning Progress", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.pack(fill='x', pady=(0, 20))

        # Stats labels
        self.total_words_label = ttk.Label(stats_frame, text="Total Words: 0", 
                                          font=("Arial", 12))
        self.total_words_label.grid(row=0, column=0, sticky='w', padx=10)

        self.reviewed_words_label = ttk.Label(stats_frame, text="Words Reviewed: 0", 
                                             font=("Arial", 12))
        self.reviewed_words_label.grid(row=0, column=1, sticky='w', padx=10)

        self.accuracy_label = ttk.Label(stats_frame, text="Overall Accuracy: 0%", 
                                       font=("Arial", 12))
        self.accuracy_label.grid(row=1, column=0, sticky='w', padx=10)

        self.streak_label = ttk.Label(stats_frame, text="Current Streak: 0 days", 
                                     font=("Arial", 12))
        self.streak_label.grid(row=1, column=1, sticky='w', padx=10)

        # Progress details frame
        details_frame = ttk.LabelFrame(main_frame, text="Word Progress Details", padding="10")
        details_frame.pack(fill='both', expand=True)

        # Treeview for detailed progress
        columns = ('Word', 'Attempts', 'Correct', 'Accuracy', 'Last Reviewed')
        self.tree = ttk.Treeview(details_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        # Refresh button
        refresh_btn = ttk.Button(main_frame, text="Refresh", command=self.load_progress_data)
        refresh_btn.pack(pady=10)

    def load_progress_data(self):
        try:
            # Get all words
            all_words = self.vocab_model.get_all_words()
            total_words = len(all_words)
            
            # Get progress data
            progress_data = list(self.progress_model.collection.find())
            reviewed_words = len(progress_data)
            
            # Calculate overall accuracy
            total_attempts = sum(p.get('attempts', 0) for p in progress_data)
            total_correct = sum(p.get('correct_answers', 0) for p in progress_data)
            overall_accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0

            # Update statistics labels
            self.total_words_label.config(text=f"Total Words: {total_words}")
            self.reviewed_words_label.config(text=f"Words Reviewed: {reviewed_words}")
            self.accuracy_label.config(text=f"Overall Accuracy: {overall_accuracy:.1f}%")
            self.streak_label.config(text="Current Streak: 0 days")  # Placeholder

            # Clear existing items in treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Create word lookup dictionary
            word_dict = {str(word['_id']): word for word in all_words}

            # Populate treeview with progress details
            for progress in progress_data:
                word_id = progress.get('word_id')
                word_info = word_dict.get(word_id)
                
                if word_info:
                    word_text = word_info['word']
                    attempts = progress.get('attempts', 0)
                    correct = progress.get('correct_answers', 0)
                    accuracy = progress.get('accuracy', 0)
                    last_reviewed = progress.get('last_reviewed', 'Never')
                    
                    if isinstance(last_reviewed, datetime):
                        last_reviewed = last_reviewed.strftime('%Y-%m-%d %H:%M')
                    
                    self.tree.insert('', 'end', values=(
                        word_text, attempts, correct, f"{accuracy:.1f}%", last_reviewed
                    ))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load progress data: {str(e)}")