@echo off 
echo ====================================== 
echo   VOCABULARY LEARNING APP 
echo ====================================== 
echo. 
echo Checking MongoDB status... 
net start MongoDB 2>nul 
if %errorlevel% equ 0 ( 
    echo MongoDB is running! 
) else ( 
    echo MongoDB is not running. Starting MongoDB... 
    net start MongoDB 
    if %errorlevel% neq 0 ( 
        echo ERROR: Cannot start MongoDB! 
        echo Please install MongoDB Community Server first. 
        echo Download: https://www.mongodb.com/try/download/community 
        pause 
        exit /b 1 
    ) 
) 
echo. 
echo Starting Vocabulary Learning App... 
VocabularyLearningApp.exe 
