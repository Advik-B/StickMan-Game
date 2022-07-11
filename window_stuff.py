from screeninfo import get_monitors

monitor = get_monitors()[0]

GAME_WIDTH = monitor.width
GAME_HEIGHT = monitor.height