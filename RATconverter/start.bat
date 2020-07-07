@echo off
set PATH=%PATH%;%~dp0
set START_DIR=%~dp0
set SCRIPT=%START_DIR%launcher.py


start C:\Python27\pythonw.exe %SCRIPT%
