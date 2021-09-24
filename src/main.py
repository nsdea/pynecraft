import game

import os
import time
import keyboard
import pyscreenshot

def terminate(*args, **kwargs):
    os._exit(0)

def screenshot(*args, **kwargs):
    shot = pyscreenshot.grab()
    shot.save(f'screenshots/{time.time()}.png')

keyboard.add_hotkey('alt+q', terminate, args=('bar'))
keyboard.add_hotkey('F2', screenshot, args=('foo'))

game.main()