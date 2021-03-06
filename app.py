import json
import sys
import os
import random
from time import sleep
from math import sin, cos, radians

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from rich.console import Console
from rich.traceback import install

c = Console(color_system="truecolor", file=sys.stdout, record=True)
install(console=c, extra_lines=5, indent_guides=True, show_locals=True)

c.log("[b magenta]Loading PyGame(SDL2)...[/]")
import pygame

c.log("[b magenta]Loaded PyGame(SDL2): [/]")
c.log("[b yellow]PyGame Version[/]:", pygame.__version__)
SDL = pygame.version.get_sdl_version()
c.log("[b blue]SDL Version[/]:", f"{SDL[0]}.{SDL[1]}.{SDL[2]}")
del SDL

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
    pygame.display.set_caption("StickMan Game")
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
    "legs": {
        "left": {"y": 100, "x": 100, "color": COLORS["blurple"], "rotation": 0},
        "right": {"y": 100, "x": 100, "color": COLORS["blurple"], "rotation": 0},
        "width": 10,
        "height": 100,
    },
}

player_movement = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
}

player_speed = 5

points = []
point_precesion = 5
point_radius = 6
border_radius = 10

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

    if KEY_PRESSED == pygame.K_SPACE:
        points.append(
            {
                "x": player1["body"]["x"] + player1["body"]["width"] - point_precesion,
                "y": player1["body"]["y"] + player1["body"]["height"] + point_precesion,
            }
        )
        c.log("[b yellow]Point added[/]")
        c.log("[b yellow]Points:[/]", points)

    if KEY_PRESSED == pygame.K_BACKSPACE:
        try:
            points.pop(-1)
            c.log("[b yellow]Point removed[/]")
            c.log("[b yellow]Points:[/]", points)
        except IndexError:
            c.log("[b yellow]No points to remove[/]")
            c.log("[b yellow]Points:[/]", points)

    if KEY_PRESSED == pygame.K_c:
        crash()


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
    # sleep(0.05) #HACK: Use this to simulate a lag


def update_player1():
    global player1
    # Set the player1's position according to the head's position
    player1["body"]["y"] = player1["head"]["y"] + player1["head"]["radius"]
    player1["body"]["x"] = player1["head"]["x"] - player1["body"]["width"] / 2
    # Set the player1's legs position according to the body's position
    player1["legs"]["left"]["y"] = player1["body"]["y"] + player1["body"]["height"]
    player1["legs"]["left"]["x"] = player1["body"]["x"] - player1["legs"]["width"]
    player1["legs"]["right"]["y"] = player1["body"]["y"] + player1["body"]["height"]
    player1["legs"]["right"]["x"] = player1["body"]["x"] + player1["body"]["width"]
    if player_movement["up"]:
        player1["head"]["y"] -= player_speed
    if player_movement["down"]:
        player1["head"]["y"] += player_speed
    if player_movement["left"]:
        player1["head"]["x"] -= player_speed
        if player1["legs"]["left"]["rotation"] > -40:
            player1["legs"]["left"]["rotation"] -= player_speed
        else:
            player1["legs"]["left"]["rotation"] += player_speed
    if player_movement["right"]:
        player1["head"]["x"] += player_speed
        if player1["legs"]["right"]["rotation"] < 40:
            player1["legs"]["right"]["rotation"] += player_speed
        else:
            player1["legs"]["right"]["rotation"] -= player_speed
    # player1["legs"]["left"]["rotation"] += player_speed

def crash():
    raise Exception("Crashed because of pressing C (custom crash)")

def draw_stuff():
    update_player1()
    for point in points:
        pygame.draw.circle(
            screen,
            COLORS["yellow"],
            (point["x"], point["y"]),
            point_radius,
        )
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
        border_radius=10,
    )
    left_leg_surface = pygame.Surface(
        (player1["legs"]["width"], player1["legs"]["height"])
    )
    left_leg_surface.fill(WINDOW["BACKGROUND_COLOR"])
    pygame.draw.rect(
        left_leg_surface,
        COLORS["lime"],
        (
            0,
            0,
            player1["legs"]["width"],
            player1["legs"]["height"],
        ),
        border_radius=10,
    )
    screen.blit(
        left_leg_surface,
        (
            player1["legs"]["left"]["x"],
            player1["legs"]["left"]["y"],
        ),
    )
    right_leg_surface = pygame.Surface(
        (player1["legs"]["width"], player1["legs"]["height"])
    )
    right_leg_surface.fill(WINDOW["BACKGROUND_COLOR"])
    pygame.draw.rect(
        right_leg_surface,
        COLORS["lime"],
        (
            0,
            0,
            player1["legs"]["width"],
            player1["legs"]["height"],
        ),
        border_radius=10,
    )
    right_leg_surface = pygame.transform.rotate(right_leg_surface, player1["legs"]["right"]["rotation"])
    right_leg_surface.set_colorkey(WINDOW["BACKGROUND_COLOR"])
    screen.blit(
        right_leg_surface,
        (
            player1["legs"]["right"]["x"],
            player1["legs"]["right"]["y"],
        ),
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
        border_radius=10,
    )
    left_leg_surface = pygame.transform.rotate(
        left_leg_surface, player1["legs"]["left"]["rotation"]
    )
    right_leg_surface = pygame.Surface(
        (player1["legs"]["width"], player1["legs"]["height"])
    )
    pygame.draw.rect(
        right_leg_surface,
        COLORS["lime"],
        (
            0,
            0,
            player1["legs"]["width"],
            player1["legs"]["height"],
        ),
        border_radius=10,
    )
    screen.blit(
        left_leg_surface,
        (
            player1["legs"]["left"]["x"],
            player1["legs"]["left"]["y"],
        ),
    )
    right_leg_surface = pygame.transform.rotate(
        right_leg_surface, player1["legs"]["right"]["rotation"]
    )
    right_leg_surface.set_colorkey(WINDOW["BACKGROUND_COLOR"])
    screen.blit(
        right_leg_surface,
        (
            player1["legs"]["right"]["x"],
            player1["legs"]["right"]["y"],
        ),
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
        border_radius=10,
    )
    left_leg_surface = pygame.transform.rotate(
        left_leg_surface, player1["legs"]["left"]["rotation"]
    )
    right_leg_surface = pygame.Surface(
        (player1["legs"]["width"], player1["legs"]["height"])
    )
    pygame.draw.rect(
        right_leg_surface,
        COLORS["lime"],
        (
            0,
            0,
            player1["legs"]["width"],
            player1["legs"]["height"],
        ),
        border_radius=10,
    )
    # right_leg_surface.fill(WINDOW["BACKGROUND_COLOR"])
    # right_leg_surface = pygame.transform.rotate(
    #     right_leg_surface, player1["legs"]["right"]["rotation"]
    # )
    # screen.blit(left_leg_surface, (player1["legs"]["left"]["x"], player1["legs"]["left"]["y"]))
    # screen.blit(right_leg_surface, (player1["legs"]["right"]["x"], player1["legs"]["right"]["y"]))


    # pygame.draw.rect(
    #     screen,
    #     COLORS["aqua"],

    #     (
    #         player1["legs"]["left"]["x"],
    #         player1["legs"]["left"]["y"],
    #         player1["legs"]["width"],
    #         player1["legs"]["height"],
    #     ),
    #     border_radius=10,
    # )
    # pygame.draw.rect(
    #     screen,
    #     COLORS["aqua"],
    #     (
    #         player1["legs"]["right"]["x"],
    #         player1["legs"]["right"]["y"],
    #         player1["legs"]["width"],
    #         player1["legs"]["height"],
    #     ),
    #     border_radius=10,
    # )
    # Draw the legs with rotation using the pygame.transform.rotate function


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
        c.log("[b green]Thanks for playing![/]")
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

    sys.exit(0)
