@echo off
chcp 1251 >nul
title Сборка AutoClicker

echo ========================================
echo    СБОРКА AUTOCLICKER
echo ========================================
echo.

:: Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python не установлен!
    echo Скачайте с https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python найден
echo.

:: Установка библиотек
echo Установка библиотек...
pip install pyautogui pillow opencv-python pygetwindow psutil pyinstaller
if errorlevel 1 (
    echo [ERROR] Ошибка при установке библиотек
    pause
    exit /b 1
)
echo [OK] Библиотеки установлены
echo.

:: Сборка EXE с добавлением папки assets
echo Сборка EXE файла...
pyinstaller --onefile --windowed --icon=assets/icon.ico --name=AutoClicker --add-data "assets;assets" src/clicker.py
if errorlevel 1 (
    echo [ERROR] Ошибка при сборке
    pause
    exit /b 1
)
echo [OK] EXE файл создан
echo.

:: Копирование файлов из assets в dist
echo Копирование файлов кнопок...
if exist assets\button.png copy assets\button.png dist\ >nul
if exist assets\stars.png copy assets\stars.png dist\ >nul
if exist assets\icon.ico copy assets\icon.ico dist\ >nul
echo [OK] Файлы скопированы
echo.

:: Создание README
echo Создание README...
echo AutoClicker > dist\README.txt
echo ========== >> dist\README.txt
echo. >> dist\README.txt
echo 1. Запустите AutoClicker.exe >> dist\README.txt
echo 2. Выберите нужные задачи >> dist\README.txt
echo 3. Нажмите СТАРТ >> dist\README.txt
echo. >> dist\README.txt
echo Необходимые файлы: assets\button.png, assets\stars.png >> dist\README.txt
echo [OK] README создан
echo.

echo ========================================
echo    СБОРКА ЗАВЕРШЕНА!
echo ========================================
echo.
echo EXE файл: dist\AutoClicker.exe
echo.
dir dist\
echo.
pause