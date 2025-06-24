@echo off
echo Creating release package...

REM Tạo thư mục release
if exist release rmdir /s /q release
mkdir release
cd release

REM Copy file executable
copy ..\dist\VocabularyLearningApp.exe .

REM Tạo file khởi động tự động MongoDB
echo @echo off > start_app.bat
echo echo ====================================== >> start_app.bat
echo echo   VOCABULARY LEARNING APP >> start_app.bat
echo echo ====================================== >> start_app.bat
echo echo. >> start_app.bat
echo echo Checking MongoDB status... >> start_app.bat
echo net start MongoDB 2^>nul >> start_app.bat
echo if %%errorlevel%% equ 0 ( >> start_app.bat
echo     echo MongoDB is running! >> start_app.bat
echo ) else ( >> start_app.bat
echo     echo MongoDB is not running. Starting MongoDB... >> start_app.bat
echo     net start MongoDB >> start_app.bat
echo     if %%errorlevel%% neq 0 ( >> start_app.bat
echo         echo ERROR: Cannot start MongoDB! >> start_app.bat
echo         echo Please install MongoDB Community Server first. >> start_app.bat
echo         echo Download: https://www.mongodb.com/try/download/community >> start_app.bat
echo         pause >> start_app.bat
echo         exit /b 1 >> start_app.bat
echo     ) >> start_app.bat
echo ) >> start_app.bat
echo echo. >> start_app.bat
echo echo Starting Vocabulary Learning App... >> start_app.bat
echo VocabularyLearningApp.exe >> start_app.bat

REM Tạo file hướng dẫn
echo VOCABULARY LEARNING APP > README.txt
echo ======================= >> README.txt
echo. >> README.txt
echo CACH SU DUNG: >> README.txt
echo 1. Chay file start_app.bat >> README.txt
echo 2. Hoac chay truc tiep VocabularyLearningApp.exe >> README.txt
echo    (can dam bao MongoDB da khoi dong) >> README.txt
echo. >> README.txt
echo YEU CAU HE THONG: >> README.txt
echo - Windows 10/11 >> README.txt
echo - MongoDB Community Server >> README.txt
echo. >> README.txt
echo CAI DAT MONGODB: >> README.txt
echo 1. Tai tu: https://www.mongodb.com/try/download/community >> README.txt
echo 2. Chon Windows x64, MSI >> README.txt
echo 3. Cai dat voi cac tuy chon mac dinh >> README.txt
echo 4. Dam bao "Install MongoDB as a Service" duoc chon >> README.txt
echo. >> README.txt
echo TINH NANG: >> README.txt
echo - Them tu vung voi tra cuu tu dong >> README.txt
echo - Flashcard system >> README.txt
echo - Quiz voi nhieu dang cau hoi >> README.txt
echo - Theo doi tien do hoc tap >> README.txt
echo - Quan ly tu vung >> README.txt

REM Tạo file khắc phục sự cố
echo KHAC PHUC SU CO > TROUBLESHOOTING.txt
echo =============== >> TROUBLESHOOTING.txt
echo. >> TROUBLESHOOTING.txt
echo 1. UNG DUNG KHONG MO DUOC: >> TROUBLESHOOTING.txt
echo    - Kiem tra Windows Defender/Antivirus >> TROUBLESHOOTING.txt
echo    - Click phai vao file .exe ^> Properties ^> Unblock >> TROUBLESHOOTING.txt
echo    - Chay bang quyen Administrator >> TROUBLESHOOTING.txt
echo. >> TROUBLESHOOTING.txt
echo 2. KHONG KET NOI DUOC DATABASE: >> TROUBLESHOOTING.txt
echo    - Kiem tra MongoDB service: >> TROUBLESHOOTING.txt
echo      net start MongoDB >> TROUBLESHOOTING.txt
echo    - Neu loi, cai lai MongoDB >> TROUBLESHOOTING.txt
echo. >> TROUBLESHOOTING.txt
echo 3. KHONG TRA CUU DUOC TU DIEN: >> TROUBLESHOOTING.txt
echo    - Kiem tra ket noi Internet >> TROUBLESHOOTING.txt
echo    - Su dung che do "Quick Add" thay the >> TROUBLESHOOTING.txt
echo. >> TROUBLESHOOTING.txt
echo 4. UNG DUNG CHAY CHAM: >> TROUBLESHOOTING.txt
echo    - Bo tick "Auto lookup English meaning" >> TROUBLESHOOTING.txt
echo    - Su dung nut "Quick Add (No Lookup)" >> TROUBLESHOOTING.txt

cd ..
echo.
echo ====================================== 
echo Release package created successfully!
echo ====================================== 
echo.
echo Contents:
echo - VocabularyLearningApp.exe (Main application)
echo - start_app.bat (Auto-start script)
echo - README.txt (User guide in Vietnamese)
echo - TROUBLESHOOTING.txt (Troubleshooting guide)
echo.
echo To use: Run start_app.bat
echo Location: release folder
echo.
pause