import tkinter as tk
from tkinter import ttk, messagebox
import config

class EditWordWindow:
    def __init__(self, master, word_data, vocab_model, on_update_callback=None):
        self.master = master
        self.word_data = word_data
        self.vocab_model = vocab_model
        self.on_update_callback = on_update_callback
        
        self.master.title("Edit Word")
        self.master.geometry("500x400")
        self.master.resizable(False, False)
        self.master.transient()
        self.master.grab_set()
        
        # Center the window
        self.master.geometry("+%d+%d" % (
            self.master.winfo_screenwidth() // 2 - 250,
            self.master.winfo_screenheight() // 2 - 200
        ))
        
        self.create_widgets()
        self.load_word_data()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(fill='both', expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Edit Word", 
                               font=("Times New Roman", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # Input fields frame
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill='x', pady=(0, 20))

        # English Word
        ttk.Label(fields_frame, text="English Word:", 
                 font=("Times New Roman", 12)).grid(row=0, column=0, sticky='w', pady=8)
        self.word_entry = ttk.Entry(fields_frame, width=30, font=("Times New Roman", 12))
        self.word_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=8)

        # Part of Speech
        ttk.Label(fields_frame, text="Part of Speech:", 
                 font=("Times New Roman", 12)).grid(row=1, column=0, sticky='w', pady=8)
        self.pos_var = tk.StringVar()
        self.pos_combo = ttk.Combobox(fields_frame, textvariable=self.pos_var, 
                                     values=config.PARTS_OF_SPEECH, 
                                     font=("Times New Roman", 12), width=28)
        self.pos_combo.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=8)

        # Vietnamese Meaning
        ttk.Label(fields_frame, text="Vietnamese Meaning:", 
                 font=("Times New Roman", 12)).grid(row=2, column=0, sticky='w', pady=8)
        self.vn_meaning_entry = ttk.Entry(fields_frame, width=30, font=("Times New Roman", 12))
        self.vn_meaning_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=8)

        # English Meaning
        ttk.Label(fields_frame, text="English Meaning:", 
                 font=("Times New Roman", 12)).grid(row=3, column=0, sticky='w', pady=8)
        self.en_meaning_text = tk.Text(fields_frame, height=3, width=30, 
                                      font=("Times New Roman", 12), wrap=tk.WORD)
        self.en_meaning_text.grid(row=3, column=1, sticky='ew', padx=(10, 0), pady=8)

        # Pronunciation
        ttk.Label(fields_frame, text="Pronunciation:", 
                 font=("Times New Roman", 12)).grid(row=4, column=0, sticky='w', pady=8)
        self.pronunciation_entry = ttk.Entry(fields_frame, width=30, font=("Times New Roman", 12))
        self.pronunciation_entry.grid(row=4, column=1, sticky='ew', padx=(10, 0), pady=8)

        # Example
        ttk.Label(fields_frame, text="Example:", 
                 font=("Times New Roman", 12)).grid(row=5, column=0, sticky='w', pady=8)
        self.example_text = tk.Text(fields_frame, height=2, width=30, 
                                   font=("Times New Roman", 12), wrap=tk.WORD)
        self.example_text.grid(row=5, column=1, sticky='ew', padx=(10, 0), pady=8)

        fields_frame.columnconfigure(1, weight=1)

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='x', pady=20)

        ttk.Button(buttons_frame, text="Save Changes", 
                  command=self.save_changes).pack(side='left', padx=(0, 10))
        ttk.Button(buttons_frame, text="Cancel", 
                  command=self.cancel).pack(side='left')

    def load_word_data(self):
        """Load existing word data into the form"""
        self.word_entry.insert(0, self.word_data.get('word', ''))
        self.pos_var.set(self.word_data.get('part_of_speech', ''))
        self.vn_meaning_entry.insert(0, self.word_data.get('vietnamese_meaning', ''))
        
        # Load text fields
        en_meaning = self.word_data.get('english_meaning', '')
        if en_meaning:
            self.en_meaning_text.insert(1.0, en_meaning)
            
        pronunciation = self.word_data.get('pronunciation', '')
        if pronunciation:
            self.pronunciation_entry.insert(0, pronunciation)
            
        example = self.word_data.get('example', '')
        if example:
            self.example_text.insert(1.0, example)

    def save_changes(self):
        """Save the edited word"""
        word = self.word_entry.get().strip()
        vn_meaning = self.vn_meaning_entry.get().strip()
        
        if not word or not vn_meaning:
            messagebox.showwarning("Warning", "Please enter both English word and Vietnamese meaning!")
            return

        try:
            updated_data = {
                'word': word.lower(),
                'vietnamese_meaning': vn_meaning,
                'part_of_speech': self.pos_var.get(),
                'english_meaning': self.en_meaning_text.get(1.0, tk.END).strip(),
                'pronunciation': self.pronunciation_entry.get().strip(),
                'example': self.example_text.get(1.0, tk.END).strip()
            }

            # Update in database
            result = self.vocab_model.update_word(str(self.word_data['_id']), updated_data)
            
            if result.modified_count > 0:
                messagebox.showinfo("Success", "Word updated successfully!")
                if self.on_update_callback:
                    self.on_update_callback()
                self.master.destroy()
            else:
                messagebox.showerror("Error", "Failed to update word!")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def cancel(self):
        """Cancel editing and close window"""
        self.master.destroy()