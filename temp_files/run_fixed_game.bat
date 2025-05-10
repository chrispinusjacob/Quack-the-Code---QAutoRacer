@echo off
echo Fixing game files...

REM Backup original file
copy game_objects.py game_objects.bak

REM Replace with fixed version
copy game_objects_fixed.py game_objects.py

echo Starting game...
python game_manager.py

REM Restore original file
copy game_objects.bak game_objects.py
del game_objects.bak

pause