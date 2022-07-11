from rich.console import Console
from rich.traceback import install
import sys
c = Console(color_system="truecolor", file=sys.stdout, record=True)

install(console=c, extra_lines=5, indent_guides=True, show_locals=True)
import pygame
from window_stuff import GAME_WIDTH, GAME_HEIGHT

WINDOW = {
    "width": GAME_WIDTH,
    "height": GAME_HEIGHT,
    "resizable": False,
    "fullscreen": True,
    "VSync": pygame.DOUBLEBUF,
    "BACKGROUND_COLOR": (39, 41, 46),
}

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
    pygame.display.update()


def draw_stuff():
    pass


def main():
    while GAME_IS_RUNNING:
        # Events
        do_event_loop()
        # Draw stuff
        draw_stuff()
        # Update screen
        update_game_screen()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        c.log("Why did you press Ctrl+C?, Why din't you close the game normally?")

    except BaseException:
        c.print_exception()
        c.log("Game crashed, please report this to the developer (advik.b@gmail.com)")
        sys.exit(1)

    finally:
        sys.exit(0)