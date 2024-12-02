@echo off
title Dependency Checker
color 01

REM Welcome message
echo ==========================================
echo.        Welcome to the Dependency Checker!
echo ==========================================
echo.
echo This script will ensure all necessary dependencies 
echo are installed and up-to-date.
echo Please make sure you are connected to the internet.
echo.
pause

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and rerun this script.
    pause
    exit /b
)

REM Check if pip is installed
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip not found. Attempting to install pip...

    REM Download get-pip.py
    echo Downloading get-pip.py...
    curl -O https://bootstrap.pypa.io/get-pip.py

    REM Run get-pip.py with Python
    python get-pip.py
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to install pip. Please install pip manually and rerun this script.
        pause
        exit /b
    )
    echo pip installed successfully.
) ELSE (
    REM Update pip if it's already installed
    echo Checking for pip updates...
    python -m pip install --upgrade pip
    echo pip is updated to the latest version.
)

REM Install each package with specified versions
echo Installing packages with specified versions...

pip install opencv-python
pip install easyocr
pip install customtkinter
pip install Pillow
pip install gTTS
pip install mysql-connector-python
pip install requests
pip uninstall numpy opencv-python
pip install numpy opencv-python
pip install --upgrade numpy opencv-python
pip install numpy==1.23.4 opencv-python==4.6.0.66
pip cache purge
pip install numpy opencv-python
pip install threading
pip install easyocr torch torchvision
pip install uuid

echo.
echo ==========================================
echo.         Installation Complete!
echo ==========================================
pause
