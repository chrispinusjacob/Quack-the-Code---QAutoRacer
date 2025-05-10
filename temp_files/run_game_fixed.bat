@echo off  
echo Adding missing constants...  
set PYTHONPATH=%PYTHONPATH%;c:\Users\ADMIN\Desktop\QAutoGame  
python -c \"import sys; f=open('game_objects_fixed.py','w'); f.write('PLAYER_SPEED = 5\\nINITIAL_ENEMY_SPEED = 3\\n'); f.write(open('game_objects.py').read()); f.close()\"  
python game_manager.py  
pause 
