import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src.database.models import VocabularyModel, ProgressModel
from src.services.dictionary_service import DictionaryService
from src.gui.flashcard_window import FlashcardWindow
from src.gui.quiz_window import QuizWindow
from src.gui.progress_window import ProgressWindow
from src.gui.vocabulary_management_window import VocabularyManagementWindow
from src.gui.edit_word_window import EditWordWindow
import config
import threading
from datetime import datetime

class MainWindow:
    def __init__(self, master, db_connection=None):
        self.master = master
        self.db_connection = db_connection
        self.db = db_connection.db if db_connection is not None else None
        self.vocab_model = VocabularyModel(self.db) if self.db is not None else None
        self.progress_model = ProgressModel(self.db) if self.db is not None else None
        self.dictionary_service = DictionaryService()
        self.recent_words = []
        
        self.master.title(config.APP_TITLE)
        self.master.geometry("1000x700")
        self.master.resizable(True, True)

        # Configure default font
        self.default_font = ("Times New Roman", 12)
        self.title_font = ("Times New Roman", 20, "bold")
        self.label_font = ("Times New Roman", 12)
        
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
        features_menu.add_command(label="Manage Vocabulary", command=self.manage_vocabulary)

    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self.master)
        main_container.pack(fill='both', expand=True, padx=15, pady=15)

        # Title
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill='x', pady=(0, 25))
        
        title_label = ttk.Label(title_frame, text="Vocabulary Learning App", 
                               font=self.title_font)
        title_label.pack()

        # Input section
        input_frame = ttk.LabelFrame(main_container, text="Add New Word", padding="15")
        input_frame.pack(fill='x', pady=(0, 25))

        # Word input
        ttk.Label(input_frame, text="English Word:", font=self.label_font).grid(row=0, column=0, sticky='w', pady=8)
        self.word_entry = ttk.Entry(input_frame, width=30, font=self.default_font)
        self.word_entry.grid(row=0, column=1, sticky='ew', padx=(15, 0), pady=8)
        self.word_entry.bind('<Return>', self.add_word_enter)

        # Part of speech
        ttk.Label(input_frame, text="Part of Speech:", font=self.label_font).grid(row=1, column=0, sticky='w', pady=8)
        self.pos_var = tk.StringVar()
        self.pos_combo = ttk.Combobox(input_frame, textvariable=self.pos_var, 
                                     values=config.PARTS_OF_SPEECH, width=28, font=self.default_font)
        self.pos_combo.grid(row=1, column=1, sticky='ew', padx=(15, 0), pady=8)

        # Vietnamese meaning
        ttk.Label(input_frame, text="Vietnamese Meaning:", font=self.label_font).grid(row=2, column=0, sticky='w', pady=8)
        self.vn_meaning_entry = ttk.Entry(input_frame, width=30, font=self.default_font)
        self.vn_meaning_entry.grid(row=2, column=1, sticky='ew', padx=(15, 0), pady=8)
        self.vn_meaning_entry.bind('<Return>', self.add_word_enter)

        # Checkbox for auto lookup
        self.auto_lookup_var = tk.BooleanVar(value=True)
        self.auto_lookup_cb = ttk.Checkbutton(input_frame, text="Auto lookup English meaning", 
                                             variable=self.auto_lookup_var)
        self.auto_lookup_cb.grid(row=3, column=1, sticky='w', pady=8)

        # Buttons frame
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=4, column=1, sticky='ew', pady=15)

        self.add_btn = ttk.Button(btn_frame, text="Add Word", command=self.add_word)
        self.add_btn.pack(side='left')

        self.quick_add_btn = ttk.Button(btn_frame, text="Quick Add (No Lookup)", 
                                       command=self.quick_add_word)
        self.quick_add_btn.pack(side='left', padx=(15, 0))

        # Status label
        self.status_label = ttk.Label(input_frame, text="", foreground="green", font=self.default_font)
        self.status_label.grid(row=5, column=0, columnspan=2, pady=8)

        input_frame.columnconfigure(1, weight=1)

        # Main content area
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill='both', expand=True)

        # Left panel - Recent words with table
        left_panel = ttk.LabelFrame(content_frame, text="Recent Words", padding="15")
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 15))

        # Recent words table
        self.create_recent_words_table(left_panel)

        # Right panel - Search and Features
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side='right', fill='y')

        # Search section
        search_frame = ttk.LabelFrame(right_panel, text="Search", padding="15")
        search_frame.pack(fill='x', pady=(0, 15))

        ttk.Label(search_frame, text="Search words:", font=self.label_font).pack(anchor='w')
        self.search_entry = ttk.Entry(search_frame, width=25, font=self.default_font)
        self.search_entry.pack(fill='x', pady=(5, 10))
        self.search_entry.bind('<KeyRelease>', self.search_words)

        ttk.Button(search_frame, text="Clear Search", command=self.clear_search).pack()

        # Features section
        features_frame = ttk.LabelFrame(right_panel, text="Features", padding="15")
        features_frame.pack(fill='x')

        ttk.Button(features_frame, text="Start Flashcards", 
                  command=self.open_flashcard_window, width=22).pack(pady=5)
        ttk.Button(features_frame, text="Take Quiz", 
                  command=self.open_quiz_window, width=22).pack(pady=5)
        ttk.Button(features_frame, text="View Progress", 
                  command=self.open_progress_window, width=22).pack(pady=5)
        ttk.Button(features_frame, text="Manage All Words", 
                  command=self.manage_vocabulary, width=22).pack(pady=5)

    def create_recent_words_table(self, parent):
        """Create a table for recent words"""
        # Table frame
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill='both', expand=True)

        # Treeview for recent words
        columns = ('Word', 'Vietnamese', 'Part of Speech', 'Date')
        self.recent_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        # Define headings
        self.recent_tree.heading('Word', text='English Word')
        self.recent_tree.heading('Vietnamese', text='Vietnamese Meaning')
        self.recent_tree.heading('Part of Speech', text='Part of Speech')
        self.recent_tree.heading('Date', text='Added Date')
        
        # Column widths
        self.recent_tree.column('Word', width=120)
        self.recent_tree.column('Vietnamese', width=180)
        self.recent_tree.column('Part of Speech', width=100)
        self.recent_tree.column('Date', width=100)

        # Configure treeview style
        style = ttk.Style()
        style.configure("Treeview", font=("Times New Roman", 11))
        style.configure("Treeview.Heading", font=("Times New Roman", 12, "bold"))

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.recent_tree.yview)
        self.recent_tree.configure(yscrollcommand=scrollbar.set)

        # Pack components
        self.recent_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Buttons for table actions
        table_btn_frame = ttk.Frame(parent)
        table_btn_frame.pack(fill='x', pady=(15, 0))

        ttk.Button(table_btn_frame, text="Edit Selected", 
                  command=self.edit_selected_word).pack(side='left', padx=(0, 10))
        ttk.Button(table_btn_frame, text="Delete Selected", 
                  command=self.delete_selected_word).pack(side='left')

        # Double-click to edit
        self.recent_tree.bind('<Double-1>', self.on_tree_double_click)

    def load_recent_words(self):
        """Load recent words into the table"""
        if not self.vocab_model:
            return
            
        # Clear existing items
        for item in self.recent_tree.get_children():
            self.recent_tree.delete(item)
            
        try:
            self.recent_words = self.vocab_model.get_recent_words(10)
            
            for word_doc in self.recent_words:
                created_date = word_doc.get('created_at', '')
                if isinstance(created_date, datetime):
                    created_date = created_date.strftime('%m/%d/%Y')
                
                self.recent_tree.insert('', 'end', values=(
                    word_doc.get('word', '').title(),
                    word_doc.get('vietnamese_meaning', ''),
                    word_doc.get('part_of_speech', ''),
                    created_date
                ), tags=(str(word_doc['_id']),))
                
        except Exception as e:
            print(f"Error loading recent words: {e}")

    def get_selected_word_from_tree(self):
        """Get selected word from the recent words tree"""
        selection = self.recent_tree.selection()
        if not selection:
            return None
        
        item = self.recent_tree.item(selection[0])
        word_id = item['tags'][0]
        
        # Find word in recent_words list
        for word in self.recent_words:
            if str(word['_id']) == word_id:
                return word
        return None

    def on_tree_double_click(self, event):
        """Handle double-click on tree item"""
        self.edit_selected_word()

    def edit_selected_word(self):
        """Edit the selected word"""
        word_data = self.get_selected_word_from_tree()
        if not word_data:
            messagebox.showwarning("Warning", "Please select a word to edit!")
            return

        edit_window = tk.Toplevel(self.master)
        EditWordWindow(edit_window, word_data, self.vocab_model, self.load_recent_words)

    def delete_selected_word(self):
        """Delete the selected word"""
        word_data = self.get_selected_word_from_tree()
        if not word_data:
            messagebox.showwarning("Warning", "Please select a word to delete!")
            return

        word = word_data.get('word', '')
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete the word '{word}'?")
        if result:
            try:
                delete_result = self.vocab_model.delete_word(str(word_data['_id']))
                if delete_result.deleted_count > 0:
                    messagebox.showinfo("Success", f"Word '{word}' deleted successfully!")
                    self.load_recent_words()
                else:
                    messagebox.showerror("Error", "Failed to delete word!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def search_words(self, event=None):
        """Search words and display in table"""
        query = self.search_entry.get().strip()
        if not query:
            self.load_recent_words()
            return
            
        if not self.vocab_model:
            return

        # Clear existing items
        for item in self.recent_tree.get_children():
            self.recent_tree.delete(item)
            
        try:
            search_results = self.vocab_model.search_words(query)
            self.recent_words = search_results  # Update recent_words for edit/delete
            
            for word_doc in search_results:
                created_date = word_doc.get('created_at', '')
                if isinstance(created_date, datetime):
                    created_date = created_date.strftime('%m/%d/%Y')
                
                self.recent_tree.insert('', 'end', values=(
                    word_doc.get('word', '').title(),
                    word_doc.get('vietnamese_meaning', ''),
                    word_doc.get('part_of_speech', ''),
                    created_date
                ), tags=(str(word_doc['_id']),))
                
        except Exception as e:
            print(f"Error searching words: {e}")

    def clear_search(self):
        """Clear search and show recent words"""
        self.search_entry.delete(0, tk.END)
        self.load_recent_words()

    # Rest of the methods remain the same...
    def add_word_enter(self, event):
        self.add_word()

    def add_word(self):
        word = self.word_entry.get().strip()
        vn_meaning = self.vn_meaning_entry.get().strip()
        pos = self.pos_var.get()

        if not word or not vn_meaning:
            messagebox.showwarning("Warning", "Please enter both English word and Vietnamese meaning!")
            return

        if not self.vocab_model:
            messagebox.showerror("Error", "Database not connected!")
            return

        self.status_label.config(text="Adding word...", foreground="blue")
        self.add_btn.config(state='disabled')
        self.quick_add_btn.config(state='disabled')

        # Check if auto lookup is enabled
        if self.auto_lookup_var.get():
            # Run dictionary lookup in separate thread
            threading.Thread(target=self._add_word_with_lookup, 
                            args=(word, vn_meaning, pos), daemon=True).start()
        else:
            # Add without lookup
            threading.Thread(target=self._add_word_without_lookup, 
                            args=(word, vn_meaning, pos), daemon=True).start()

    def quick_add_word(self):
        """Add word quickly without API lookup"""
        word = self.word_entry.get().strip()
        vn_meaning = self.vn_meaning_entry.get().strip()
        pos = self.pos_var.get()

        if not word or not vn_meaning:
            messagebox.showwarning("Warning", "Please enter both English word and Vietnamese meaning!")
            return

        if not self.vocab_model:
            messagebox.showerror("Error", "Database not connected!")
            return

        self.status_label.config(text="Adding word...", foreground="blue")
        self.add_btn.config(state='disabled')
        self.quick_add_btn.config(state='disabled')

        # Add without lookup
        threading.Thread(target=self._add_word_without_lookup, 
                        args=(word, vn_meaning, pos), daemon=True).start()

    def _add_word_without_lookup(self, word, vn_meaning, pos):
        """Add word without API lookup - faster"""
        try:
            word_data = {
                'word': word.lower(),
                'vietnamese_meaning': vn_meaning,
                'part_of_speech': pos,
                'english_meaning': '',
                'pronunciation': '',
                'example': ''
            }

            # Add to database
            result = self.vocab_model.add_word(word_data)
            
            # Update UI in main thread
            self.master.after(0, self._add_word_success, word)
            
        except Exception as e:
            self.master.after(0, self._add_word_error, str(e))

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
        self.quick_add_btn.config(state='normal')
        
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
        self.quick_add_btn.config(state='normal')

    def import_data(self):
        messagebox.showinfo("Import", "Use the Vocabulary Management window to import data!")

    def export_data(self):
        messagebox.showinfo("Export", "Use the Vocabulary Management window to export data!")

    def open_flashcard_window(self):
        if not self.vocab_model:
            messagebox.showerror("Error", "Database not connected!")
            return
            
        try:
            words = self.vocab_model.get_all_words()
            if not words:
                messagebox.showinfo("Info", "No words available for flashcards!")
                return
                
            flashcard_win = tk.Toplevel(self.master)
            FlashcardWindow(flashcard_win, words, self.progress_model)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open flashcards: {str(e)}")

    def open_quiz_window(self):
        if not self.vocab_model:
            messagebox.showerror("Error", "Database not connected!")
            return
            
        try:
            words = self.vocab_model.get_all_words()
            if not words:
                messagebox.showinfo("Info", "No words available for quiz!")
                return
                
            quiz_win = tk.Toplevel(self.master)
            QuizWindow(quiz_win, words, self.progress_model)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open quiz: {str(e)}")

    def open_progress_window(self):
        if self.progress_model is None:
            messagebox.showerror("Error", "Database not connected!")
            return
            
        try:
            progress_win = tk.Toplevel(self.master)
            ProgressWindow(progress_win, self.progress_model, self.vocab_model)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open progress window: {str(e)}")

    def manage_vocabulary(self):
        """Open vocabulary management window"""
        if not self.vocab_model:
            messagebox.showerror("Error", "Database not connected!")
            return
            
        try:
            manage_win = tk.Toplevel(self.master)
            VocabularyManagementWindow(manage_win, self.vocab_model)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open vocabulary management: {str(e)}")