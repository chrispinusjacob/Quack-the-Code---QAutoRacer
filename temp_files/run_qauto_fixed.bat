@echo off
echo Adding missing constants to QAutoGame.py...

REM Create a temporary file with the missing constants
echo import pygame > temp_constants.py
echo import sys >> temp_constants.py
echo import os >> temp_constants.py
echo import math >> temp_constants.py
echo import random >> temp_constants.py
echo import json >> temp_constants.py
echo from pygame.locals import * >> temp_constants.py
echo. >> temp_constants.py
echo # Game speeds >> temp_constants.py
echo PLAYER_SPEED = 5 >> temp_constants.py
echo INITIAL_ENEMY_SPEED = 3 >> temp_constants.py
echo INITIAL_SCROLL_SPEED = 5 >> temp_constants.py
echo. >> temp_constants.py
echo # Now include the original QAutoGame.py >> temp_constants.py

REM Append the original QAutoGame.py content
type QAutoGame.py >> temp_constants.py

REM Replace the original with the fixed version
move /y temp_constants.py QAutoGame.py

echo Running QAutoGame.py...
python QAutoGame.py

pause