import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src.database.models import VocabularyModel, ProgressModel
from src.services.dictionary_service import DictionaryService
from src.gui.flashcard_window import FlashcardWindow
from src.gui.quiz_window import QuizWindow
from src.gui.progress_window import ProgressWindow
import config
import threading

class MainWindow:
    def __init__(self, master, db_connection=None):
        self.master = master
        self.db_connection = db_connection
        self.db = db_connection.db if db_connection else None
        self.vocab_model = VocabularyModel(self.db) if self.db else None
        self.progress_model = ProgressModel(self.db) if self.db else None
        self.dictionary_service = DictionaryService()
        
        self.master.title(config.APP_TITLE)
        self.master.geometry("800x600")
        self.master.resizable(True, True)

        self.create_menu()
        self.create_widgets()
        self.load_recent_words()

    def create_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import", command=self.import_data)
        file_menu.add_command(label="Export", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        features_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Features", menu=features_menu)
        features_menu.add_command(label="Flashcards", command=self.open_flashcard_window)
        features_menu.add_command(label="Quiz", command=self.open_quiz_window)
        features_menu.add_command(label="Progress", command=self.open_progress_window)

    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self.master)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)

        # Title
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="Vocabulary Learning App", 
                               font=("Arial", 20, "bold"))
        title_label.pack()

        # Input section
        input_frame = ttk.LabelFrame(main_container, text="Add New Word", padding="10")
        input_frame.pack(fill='x', pady=(0, 20))

        # Word input
        ttk.Label(input_frame, text="English Word:").grid(row=0, column=0, sticky='w', pady=5)
        self.word_entry = ttk.Entry(input_frame, width=30, font=("Arial", 12))
        self.word_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        self.word_entry.bind('<Return>', self.add_word_enter)

        # Part of speech
        ttk.Label(input_frame, text="Part of Speech:").grid(row=1, column=0, sticky='w', pady=5)
        self.pos_var = tk.StringVar()
        self.pos_combo = ttk.Combobox(input_frame, textvariable=self.pos_var, 
                                     values=config.PARTS_OF_SPEECH, width=27)
        self.pos_combo.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)

        # Vietnamese meaning
        ttk.Label(input_frame, text="Vietnamese Meaning:").grid(row=2, column=0, sticky='w', pady=5)
        self.vn_meaning_entry = ttk.Entry(input_frame, width=30, font=("Arial", 12))
        self.vn_meaning_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
        self.vn_meaning_entry.bind('<Return>', self.add_word_enter)

        # Add button
        self.add_btn = ttk.Button(input_frame, text="Add Word", command=self.add_word)
        self.add_btn.grid(row=3, column=1, sticky='e', pady=10)

        # Status label
        self.status_label = ttk.Label(input_frame, text="", foreground="green")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=5)

        input_frame.columnconfigure(1, weight=1)

        # Main content area
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill='both', expand=True)

        # Left panel - Recent words
        left_panel = ttk.LabelFrame(content_frame, text="Recent Words (10)", padding="10")
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))

        # Recent words listbox
        listbox_frame = ttk.Frame(left_panel)
        listbox_frame.pack(fill='both', expand=True)

        self.recent_listbox = tk.Listbox(listbox_frame, font=("Arial", 10))
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.recent_listbox.yview)
        self.recent_listbox.configure(yscrollcommand=scrollbar.set)

        self.recent_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Buttons for recent words
        recent_btn_frame = ttk.Frame(left_panel)
        recent_btn_frame.pack(fill='x', pady=(10, 0))

        ttk.Button(recent_btn_frame, text="Edit", command=self.edit_selected_word).pack(side='left', padx=(0, 5))
        ttk.Button(recent_btn_frame, text="Delete", command=self.delete_selected_word).pack(side='left')

        # Right panel - Search and Features
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side='right', fill='y')

        # Search section
        search_frame = ttk.LabelFrame(right_panel, text="Search", padding="10")
        search_frame.pack(fill='x', pady=(0, 10))

        self.search_entry = ttk.Entry(search_frame, width=25)
        self.search_entry.pack(fill='x', pady=(0, 5))
        self.search_entry.bind('<KeyRelease>', self.search_words)

        ttk.Button(search_frame, text="Clear", command=self.clear_search).pack()

        # Features section
        features_frame = ttk.LabelFrame(right_panel, text="Features", padding="10")
        features_frame.pack(fill='x')

        ttk.Button(features_frame, text="Start Flashcards", 
                  command=self.open_flashcard_window, width=20).pack(pady=2)
        ttk.Button(features_frame, text="Take Quiz", 
                  command=self.open_quiz_window, width=20).pack(pady=2)
        ttk.Button(features_frame, text="View Progress", 
                  command=self.open_progress_window, width=20).pack(pady=2)
        ttk.Button(features_frame, text="Manage All Words", 
                  command=self.manage_vocabulary, width=20).pack(pady=2)

    def add_word_enter(self, event):
        self.add_word()

    def add_word(self):
        word = self.word_entry.get().strip()
        vn_meaning = self.vn_meaning_entry.get().strip()
        pos = self.pos_var.get()

        if not word or not vn_meaning:
            messagebox.showwarning("Warning", "Please enter both English word and Vietnamese meaning!")
            return

        self.status_label.config(text="Adding word...", foreground="blue")
        self.add_btn.config(state='disabled')

        # Run dictionary lookup in separate thread
        threading.Thread(target=self._add_word_with_lookup, 
                        args=(word, vn_meaning, pos), daemon=True).start()

    def _add_word_with_lookup(self, word, vn_meaning, pos):
        try:
            # Get English definition and pronunciation
            word_info = self.dictionary_service.get_word_info(word)
            
            word_data = {
                'word': word.lower(),
                'vietnamese_meaning': vn_meaning,
                'part_of_speech': pos,
                'english_meaning': word_info.get('english_meaning', ''),
                'pronunciation': word_info.get('pronunciation', ''),
                'example': word_info.get('example', '')
            }

            # Add to database
            result = self.vocab_model.add_word(word_data)
            
            # Update UI in main thread
            self.master.after(0, self._add_word_success, word)
            
        except Exception as e:
            self.master.after(0, self._add_word_error, str(e))

    def _add_word_success(self, word):
        self.status_label.config(text=f"Added '{word}' successfully!", foreground="green")
        self.add_btn.config(state='normal')
        
        # Clear inputs
        self.word_entry.delete(0, tk.END)
        self.vn_meaning_entry.delete(0, tk.END)
        self.pos_var.set('')
        
        # Refresh recent words
        self.load_recent_words()
        
        # Focus back to word entry
        self.word_entry.focus()

    def _add_word_error(self, error):
        self.status_label.config(text=f"Error: {error}", foreground="red")
        self.add_btn.config(state='normal')

    def load_recent_words(self):
        if not self.vocab_model:
            return
            
        self.recent_listbox.delete(0, tk.END)
        recent_words = self.vocab_model.get_recent_words(10)
        
        for word_doc in recent_words:
            display_text = f"{word_doc['word']} - {word_doc['vietnamese_meaning']}"
            self.recent_listbox.insert(tk.END, display_text)

    def search_words(self, event=None):
        query = self.search_entry.get().strip()
        if not query:
            self.load_recent_words()
            return
            
        if not self.vocab_model:
            return

        self.recent_listbox.delete(0, tk.END)
        search_results = self.vocab_model.search_words(query)
        
        for word_doc in search_results:
            display_text = f"{word_doc['word']} - {word_doc['vietnamese_meaning']}"
            self.recent_listbox.insert(tk.END, display_text)

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_recent_words()

    def edit_selected_word(self):
        selection = self.recent_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a word to edit!")
            return
        messagebox.showinfo("Edit", "Edit functionality to be implemented in vocabulary management window.")

    def delete_selected_word(self):
        selection = self.recent_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a word to delete!")
            return
        messagebox.showinfo("Delete", "Delete functionality to be implemented.")

    def import_data(self):
        messagebox.showinfo("Import", "Import data functionality to be implemented.")

    def export_data(self):
        messagebox.showinfo("Export", "Export data functionality to be implemented.")

    def open_flashcard_window(self):
        if not self.vocab_model:
            messagebox.showerror("Error", "Database not connected!")
            return
            
        words = self.vocab_model.get_all_words()
        if not words:
            messagebox.showinfo("Info", "No words available for flashcards!")
            return
            
        flashcard_win = tk.Toplevel(self.master)
        FlashcardWindow(flashcard_win, words, self.progress_model)

    def open_quiz_window(self):
        if not self.vocab_model:
            messagebox.showerror("Error", "Database not connected!")
            return
            
        words = self.vocab_model.get_all_words()
        if not words:
            messagebox.showinfo("Info", "No words available for quiz!")
            return
            
        quiz_win = tk.Toplevel(self.master)
        QuizWindow(quiz_win, words, self.progress_model)

    def open_progress_window(self):
        if not self.progress_model:
            messagebox.showerror("Error", "Database not connected!")
            return
            
        progress_win = tk.Toplevel(self.master)
        ProgressWindow(progress_win, self.progress_model, self.vocab_model)

    def manage_vocabulary(self):
        messagebox.showinfo("Manage", "Vocabulary management window to be implemented.")