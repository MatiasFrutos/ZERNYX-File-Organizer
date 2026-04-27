@echo off
title ZERNYX File Organizer
color 0F

echo ============================================================
echo  ZERNYX File Organizer
echo ============================================================
echo.

python --version
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta agregado al PATH.
    echo.
    pause
    exit /b
)

python zernyx_file_organizer.py

pause