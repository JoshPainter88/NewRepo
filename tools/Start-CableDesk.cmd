@echo off
rem Refresh the file index, then open Cable Desk. Keep this file next to cable-desk.html and Build-FileIndex.ps1.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Build-FileIndex.ps1" %*
if exist "%~dp0cable-desk.html" (start "" "%~dp0cable-desk.html") else (echo cable-desk.html not found next to this script.& pause)
