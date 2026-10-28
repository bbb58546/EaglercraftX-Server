@echo off
setlocal
cd /d "%~dp0.."
if not exist "server-26.2\paper.jar" (
  echo Run: py -3 modern-26.2\setup.py
  pause
  exit /b 1
)
findstr /x /c:"eula=true" "server-26.2\eula.txt" >nul
if errorlevel 1 (
  echo Read https://aka.ms/MinecraftEULA and set eula=true in server-26.2\eula.txt only if you agree.
  pause
  exit /b 1
)
cd /d "server-26.2"
java -Xms1G -Xmx3G -jar paper.jar --nogui
pause
