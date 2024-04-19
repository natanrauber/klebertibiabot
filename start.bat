@echo off

rem Run install dependencies
python -m pip install -r .\requirements.txt

rem Run compiler
python .\compiler.py

rem Read uid from uid.txt
set /p uid=<uid.txt

rem Run the executable with the generated uid
.\dist\%uid%.exe

rem Wait for uid.exe to finish before exiting
:WAIT_FOR_UID
timeout /T 1 /NOBREAK >nul
tasklist /FI "IMAGENAME eq %uid%.exe" 2>NUL | find /I /N "%uid%.exe" >NUL
if "%ERRORLEVEL%"=="0" goto WAIT_FOR_UID

rem Delete uid.txt
del uid.txt

rem Exit the batch script
exit /b
