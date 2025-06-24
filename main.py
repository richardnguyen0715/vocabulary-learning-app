import os
import sys

# Add the project root to the Python path
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_path)
print(f"Root path: {root_path}")

from src.database.connection import connect_to_database
from src.gui.main_window import MainWindow
import tkinter as tk

def main():
    try:
        # Connect to the database
        db_connection = connect_to_database()
        
        # Create the main tkinter window
        root = tk.Tk()
        
        # Create the main window (pass the root and db_connection)
        main_window = MainWindow(root, db_connection)
        
        # Start the GUI event loop
        root.mainloop()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close database connection when app closes
        if 'db_connection' in locals():
            db_connection.close()

if __name__ == "__main__":
    main()