@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo  Building MapTextureCreator executable
echo ==========================================

REM Clean previous builds
echo [INFO] Cleaning old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist bin\MapTextureCreator.exe del /f /q bin\MapTextureCreator.exe

REM Ensure bin directory exists
if not exist bin mkdir bin

REM Run PyInstaller
echo [INFO] Running PyInstaller...
pyinstaller ^
  --onefile ^
  --clean ^
  --name MapTextureCreator ^
  --distpath bin ^
  map_texture_creator.py

echo ==========================================
echo  Build completed successfully!
echo  Output: bin\MapTextureCreator.exe
echo ==========================================

pause
