@echo off

rem Run pyinstaller
pyinstaller --clean .\compiler.spec

rem Check if pyinstaller succeeded
if %errorlevel% equ 0 (
    rem If successful, run the executable
    .\dist\compiler.exe
) else (
    rem If pyinstaller failed, print an error message
    echo PyInstaller failed. Please check the logs.
)
