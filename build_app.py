import PyInstaller.__main__
import os
import sys

# Đường dẫn đến thư mục dự án
project_dir = os.path.dirname(os.path.abspath(__file__))

# Cấu hình PyInstaller
PyInstaller.__main__.run([
    '--name=VocabularyLearningApp',
    '--onefile',  # Tạo một file exe duy nhất
    '--windowed',  # Không hiển thị console
    # '--icon=icon.ico',  # Icon cho ứng dụng (tùy chọn)
    '--add-data=config.py;.',
    '--hidden-import=pymongo',
    '--hidden-import=requests',
    '--hidden-import=tkinter',
    '--hidden-import=tkinter.ttk',
    '--hidden-import=datetime',
    '--hidden-import=threading',
    '--hidden-import=json',
    '--hidden-import=csv',
    '--hidden-import=bson',
    '--distpath=dist',
    '--workpath=build',
    '--specpath=.',
    'main.py'
])