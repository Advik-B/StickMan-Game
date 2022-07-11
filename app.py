import json
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from rich.console import Console
from rich.traceback import install

c = Console(color_system="truecolor", file=sys.stdout, record=True)
install(console=c, extra_lines=5, indent_guides=True, show_locals=True)

c.log("[b magenta]Loading PyGame(SDL2)...[/]")
import pygame

from window_stuff import GAME_HEIGHT, GAME_WIDTH

c.log("[b magenta]Loading colors defined in json file...[/]")
with open("colors.json") as colors:
    COLORS = json.load(colors)

WINDOW = {
    "width": GAME_WIDTH * 0.9,
    "height": GAME_HEIGHT * 0.8,
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
c.log("[b magenta]Initialising game...[/]")
screen = pre_launch()

player1 = {
    "head": {"y": 100, "x": 100, "color": COLORS["aqua"], "radius": 32},
    "body": {
        "y": 100,
        "x": 100,
        "color": COLORS["blurple"],
        "height": 100,
        "width": 10,
    },
}

player_movement = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
}

player_speed = 5

# Functions
def do_event_loop():
    global GAME_IS_RUNNING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_IS_RUNNING = False
        if event.type == pygame.KEYDOWN:
            handle_keys_d(event.key)
        if event.type == pygame.KEYUP:
            handle_keys_u(event.key)


def handle_keys_d(KEY_PRESSED):
    if KEY_PRESSED == pygame.K_ESCAPE:
        GAME_IS_RUNNING = False
    if KEY_PRESSED == pygame.K_UP:
        player_movement["up"] = True

    if KEY_PRESSED == pygame.K_DOWN:
        player_movement["down"] = True

    if KEY_PRESSED == pygame.K_LEFT:
        player_movement["left"] = True

    if KEY_PRESSED == pygame.K_RIGHT:
        player_movement["right"] = True

def handle_keys_u(KEY_RELEASED):
    if KEY_RELEASED == pygame.K_UP:
        player_movement["up"] = False
    if KEY_RELEASED == pygame.K_DOWN:
        player_movement["down"] = False
    if KEY_RELEASED == pygame.K_LEFT:
        player_movement["left"] = False
    if KEY_RELEASED == pygame.K_RIGHT:
        player_movement["right"] = False


def update_game_screen():
    screen.fill(WINDOW["BACKGROUND_COLOR"])
    draw_stuff()
    pygame.display.update()
    pygame.display.flip()


def update_player1():
    global player1
    # Set the player1's position according to the head's position
    player1["body"]["y"] = player1["head"]["y"] + player1["head"]["radius"]
    player1["body"]["x"] = player1["head"]["x"] + (player1["head"]["radius"] - 37)
    if player_movement["up"]:
        player1["head"]["y"] -= player_speed
    if player_movement["down"]:
        player1["head"]["y"] += player_speed
    if player_movement["left"]:
        player1["head"]["x"] -= player_speed
    if player_movement["right"]:
        player1["head"]["x"] += player_speed

    # player1["head"]["y"] = WINDOW["height"] - player1["body"]["height"]


def draw_stuff():
    update_player1()
    pygame.draw.circle(
        screen,
        player1["head"]["color"],
        (player1["head"]["x"], player1["head"]["y"]),
        player1["head"]["radius"],
    )
    pygame.draw.rect(
        screen,
        player1["body"]["color"],
        (
            player1["body"]["x"],
            player1["body"]["y"],
            player1["body"]["width"],
            player1["body"]["height"],
        ),
    )


def main():
    while GAME_IS_RUNNING:
        # Events
        do_event_loop()
        # Update screen
        update_game_screen()


if __name__ == "__main__":
    try:
        c.log("[b magenta]Starting game...[/]")
        main()
    except KeyboardInterrupt:
        c.log(
            "[b]Why[/] did you press [i purple]Ctrl+C[/]?, Why din't you close the game normally?"
        )

    except BaseException:
        c.print_exception()
        c.log(
            "[b red] Game crashed[/], [i]please[/] report this to the developer [b green](https://github.com/Advik-B/StickMan-Game/issues/new/choose)[/]"
        )
        sys.exit(1)

    finally:
        c.log("[b green]Thanks for playing![/]")
        sys.exit(0)
