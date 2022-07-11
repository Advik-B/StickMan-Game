import json
import sys

from rich.console import Console
from rich.traceback import install

c = Console(color_system="truecolor", file=sys.stdout, record=True)
install(console=c, extra_lines=5, indent_guides=True, show_locals=True)
import pygame

from window_stuff import GAME_HEIGHT, GAME_WIDTH

with open("colors.json") as colors:
    COLORS = json.load(colors)

WINDOW = {
    "width": GAME_WIDTH* .9,
    "height": GAME_HEIGHT * .8,
    "resizable": False,
    "fullscreen": False,
    "VSync": pygame.DOUBLEBUF,
    "BACKGROUND_COLOR": (39, 41, 46),
}

PLAYER_COLOR = (255, 255, 255)

# Super function to initialize the game
def pre_launch():
    global screen
    pygame.init()
    pygame.display.init()
    pygame.display.set_caption("My Game")
    screen = pygame.display.set_mode((WINDOW["width"], WINDOW["height"]))

    if WINDOW["resizable"]:
        screen = pygame.display.set_mode(
            (WINDOW["width"], WINDOW["height"]), pygame.RESIZABLE, WINDOW["VSync"]
        )

    if WINDOW["fullscreen"] and not WINDOW["resizable"]:
        screen = pygame.display.set_mode(
            (WINDOW["width"], WINDOW["height"]), pygame.FULLSCREEN, WINDOW["VSync"]
        )
    return screen


# Variables
GAME_IS_RUNNING = True
screen = pre_launch()

player1 = {
    "head": {
        "y": 100,
        "x": 100,
        "color": COLORS["aqua"],
        "radius": 32
    },
    "body": {
        "y": 100,
        "x": 100,
        "color": COLORS["blurple"],
    }
}

# Functions
def do_event_loop():
    global GAME_IS_RUNNING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_IS_RUNNING = False
        if event.type == pygame.KEYDOWN:
            handle_keys(event.key)


def handle_keys(KEY_PRESSED):
    if KEY_PRESSED == pygame.K_ESCAPE:
        GAME_IS_RUNNING = False


def update_game_screen():
    screen.fill(WINDOW["BACKGROUND_COLOR"])
    draw_stuff()
    pygame.display.update()
    pygame.display.flip()

def update_player1():
    global player1
    # Set the player1's position according to the head's position
    player1["body"]["x"] = player1["head"]["x"] + (player1["head"]["radius"] - 64)
    player1["body"]["y"] = player1["head"]["y"] + player1["head"]["radius"]



def draw_stuff():
    update_player1()
    pygame.draw.circle(screen, player1["head"]["color"], (player1["head"]["x"], player1["head"]["y"]), player1["head"]["radius"])
    pygame.draw.rect(screen, player1["body"]["color"], (player1["body"]["x"], player1["body"]["y"], player1["head"]["radius"]*2, player1["head"]["radius"]*2))

def main():
    while GAME_IS_RUNNING:
        # Events
        do_event_loop()
        # Update screen
        update_game_screen()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        c.log("[b]Why[/] did you press [i purple]Ctrl+C[/]?, Why din't you close the game normally?")

    except BaseException:
        c.print_exception()
        c.log("[b red] Game crashed[/], [i]please[/] report this to the developer [b green](https://github.com/Advik-B/StickMan-Game/issues/new/choose)[/]")
        sys.exit(1)

    finally:
        sys.exit(0)
