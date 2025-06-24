import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from src.gui.edit_word_window import EditWordWindow
import json
import csv
from datetime import datetime

class VocabularyManagementWindow:
    def __init__(self, master, vocab_model):
        self.master = master
        self.vocab_model = vocab_model
        self.all_words = []
        
        self.master.title("Vocabulary Management")
        self.master.geometry("900x600")
        self.master.resizable(True, True)
        
        self.create_widgets()
        self.load_all_words()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill='both', expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Vocabulary Management", 
                               font=("Times New Roman", 18, "bold"))
        title_label.pack(pady=(0, 15))

        # Toolbar
        toolbar_frame = ttk.Frame(main_frame)
        toolbar_frame.pack(fill='x', pady=(0, 10))

        # Search frame
        search_frame = ttk.Frame(toolbar_frame)
        search_frame.pack(side='left', fill='x', expand=True)

        ttk.Label(search_frame, text="Search:", 
                 font=("Times New Roman", 12)).pack(side='left', padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame, font=("Times New Roman", 12))
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.search_words)

        ttk.Button(search_frame, text="Clear", 
                  command=self.clear_search).pack(side='left', padx=(0, 20))

        # Action buttons
        buttons_frame = ttk.Frame(toolbar_frame)
        buttons_frame.pack(side='right')

        ttk.Button(buttons_frame, text="Add New", 
                  command=self.add_new_word).pack(side='left', padx=2)
        ttk.Button(buttons_frame, text="Edit", 
                  command=self.edit_selected_word).pack(side='left', padx=2)
        ttk.Button(buttons_frame, text="Delete", 
                  command=self.delete_selected_word).pack(side='left', padx=2)
        ttk.Button(buttons_frame, text="Export", 
                  command=self.export_words).pack(side='left', padx=2)
        ttk.Button(buttons_frame, text="Import", 
                  command=self.import_words).pack(side='left', padx=2)

        # Words table
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill='both', expand=True)

        # Treeview
        columns = ('Word', 'Vietnamese', 'Part of Speech', 'Pronunciation', 'Created')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        # Define headings and column widths
        self.tree.heading('Word', text='English Word')
        self.tree.heading('Vietnamese', text='Vietnamese Meaning')
        self.tree.heading('Part of Speech', text='Part of Speech')
        self.tree.heading('Pronunciation', text='Pronunciation')
        self.tree.heading('Created', text='Created Date')
        
        self.tree.column('Word', width=150)
        self.tree.column('Vietnamese', width=200)
        self.tree.column('Part of Speech', width=120)
        self.tree.column('Pronunciation', width=120)
        self.tree.column('Created', width=120)

        # Configure fonts for treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Times New Roman", 11))
        style.configure("Treeview.Heading", font=("Times New Roman", 12, "bold"))

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack components
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", 
                                     font=("Times New Roman", 10))
        self.status_label.pack(side='bottom', fill='x', pady=(10, 0))

        # Double-click to edit
        self.tree.bind('<Double-1>', self.on_double_click)

    def load_all_words(self):
        """Load all words from database"""
        try:
            self.all_words = self.vocab_model.get_all_words()
            self.populate_tree(self.all_words)
            self.status_label.config(text=f"Loaded {len(self.all_words)} words")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load words: {str(e)}")

    def populate_tree(self, words):
        """Populate treeview with words"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add words to tree
        for word in words:
            created_date = word.get('created_at', '')
            if isinstance(created_date, datetime):
                created_date = created_date.strftime('%Y-%m-%d')
            
            self.tree.insert('', 'end', values=(
                word.get('word', '').title(),
                word.get('vietnamese_meaning', ''),
                word.get('part_of_speech', ''),
                word.get('pronunciation', ''),
                created_date
            ), tags=(str(word['_id']),))

    def search_words(self, event=None):
        """Search words based on search entry"""
        query = self.search_entry.get().strip().lower()
        if not query:
            self.populate_tree(self.all_words)
            return

        filtered_words = []
        for word in self.all_words:
            if (query in word.get('word', '').lower() or 
                query in word.get('vietnamese_meaning', '').lower() or
                query in word.get('english_meaning', '').lower()):
                filtered_words.append(word)

        self.populate_tree(filtered_words)
        self.status_label.config(text=f"Found {len(filtered_words)} words")

    def clear_search(self):
        """Clear search and show all words"""
        self.search_entry.delete(0, tk.END)
        self.populate_tree(self.all_words)
        self.status_label.config(text=f"Showing all {len(self.all_words)} words")

    def get_selected_word(self):
        """Get the selected word data"""
        selection = self.tree.selection()
        if not selection:
            return None
        
        item = self.tree.item(selection[0])
        word_id = item['tags'][0]
        
        # Find word in all_words list
        for word in self.all_words:
            if str(word['_id']) == word_id:
                return word
        return None

    def add_new_word(self):
        """Open add new word dialog"""
        messagebox.showinfo("Add New Word", "Use the main window to add new words!")

    def edit_selected_word(self):
        """Edit the selected word"""
        word_data = self.get_selected_word()
        if not word_data:
            messagebox.showwarning("Warning", "Please select a word to edit!")
            return

        edit_window = tk.Toplevel(self.master)
        EditWordWindow(edit_window, word_data, self.vocab_model, self.load_all_words)

    def delete_selected_word(self):
        """Delete the selected word"""
        word_data = self.get_selected_word()
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
                    self.load_all_words()
                else:
                    messagebox.showerror("Error", "Failed to delete word!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def export_words(self):
        """Export words to file"""
        if not self.all_words:
            messagebox.showinfo("Info", "No words to export!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.export_to_csv(file_path)
                else:
                    self.export_to_json(file_path)
                messagebox.showinfo("Success", f"Words exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def export_to_json(self, file_path):
        """Export words to JSON file"""
        export_data = []
        for word in self.all_words:
            word_dict = {
                'word': word.get('word', ''),
                'vietnamese_meaning': word.get('vietnamese_meaning', ''),
                'part_of_speech': word.get('part_of_speech', ''),
                'english_meaning': word.get('english_meaning', ''),
                'pronunciation': word.get('pronunciation', ''),
                'example': word.get('example', ''),
                'created_at': word.get('created_at', '').isoformat() if isinstance(word.get('created_at'), datetime) else str(word.get('created_at', ''))
            }
            export_data.append(word_dict)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

    def export_to_csv(self, file_path):
        """Export words to CSV file"""
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['English Word', 'Vietnamese Meaning', 'Part of Speech', 
                           'English Meaning', 'Pronunciation', 'Example', 'Created Date'])
            
            for word in self.all_words:
                created_at = word.get('created_at', '')
                if isinstance(created_at, datetime):
                    created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
                
                writer.writerow([
                    word.get('word', ''),
                    word.get('vietnamese_meaning', ''),
                    word.get('part_of_speech', ''),
                    word.get('english_meaning', ''),
                    word.get('pronunciation', ''),
                    word.get('example', ''),
                    created_at
                ])

    def import_words(self):
        """Import words from file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.import_from_csv(file_path)
                else:
                    self.import_from_json(file_path)
                self.load_all_words()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {str(e)}")

    def import_from_json(self, file_path):
        """Import words from JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        imported_count = 0
        for word_data in data:
            if word_data.get('word') and word_data.get('vietnamese_meaning'):
                try:
                    self.vocab_model.add_word(word_data)
                    imported_count += 1
                except:
                    continue
        
        messagebox.showinfo("Success", f"Imported {imported_count} words successfully!")

    def import_from_csv(self, file_path):
        """Import words from CSV file"""
        imported_count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('English Word') and row.get('Vietnamese Meaning'):
                    word_data = {
                        'word': row.get('English Word', '').lower(),
                        'vietnamese_meaning': row.get('Vietnamese Meaning', ''),
                        'part_of_speech': row.get('Part of Speech', ''),
                        'english_meaning': row.get('English Meaning', ''),
                        'pronunciation': row.get('Pronunciation', ''),
                        'example': row.get('Example', '')
                    }
                    try:
                        self.vocab_model.add_word(word_data)
                        imported_count += 1
                    except:
                        continue
        
        messagebox.showinfo("Success", f"Imported {imported_count} words successfully!")

    def on_double_click(self, event):
        """Handle double-click on tree item"""
        self.edit_selected_word()