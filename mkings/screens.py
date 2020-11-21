import pygame
import sys
from .constants import BACKGROUND, FPS, WHITE, FONTS_PATH
from .buttons import Button
from .players import Player
from .assets import Asset


class ScreenManager:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self._resizing_display = False
        self._start_menu = False
        self._game_run = False
        self._end_screen = False
        self._about_screen = False
        self._reveal_cards = False

    def start_menu(self, game, display):
        self._start_menu = True
        self._resizing_display = True
        pygame.event.clear()
        pygame.font.init()

        while self._start_menu:
            self.clock.tick(FPS)
            HINT = (
                display.HINT * 1.5
            )  # Magic number adjusts sizes without messing positions.
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H

            # BUTTONS
            if self._resizing_display:
                self._resizing_display = False
                solo = Button(
                    DISP_W * 0.5 - HINT * 0.75,
                    HINT * 0.7,
                    HINT * 0.4,
                    HINT * 0.4,
                    "players_one.png",
                    "players_one_hover.png",
                    game.choose_players,
                    1,
                )
                two = Button(
                    DISP_W * 0.5 - HINT * 0.25,
                    HINT * 0.7,
                    HINT * 0.4,
                    HINT * 0.4,
                    "players_two.png",
                    "players_two_hover.png",
                    game.choose_players,
                    2,
                )
                three = Button(
                    DISP_W * 0.5 + HINT * 0.25,
                    HINT * 0.7,
                    HINT * 0.4,
                    HINT * 0.4,
                    "players_three.png",
                    "players_three_hover.png",
                    game.choose_players,
                    3,
                )
                four = Button(
                    DISP_W * 0.5 + HINT * 0.75,
                    HINT * 0.7,
                    HINT * 0.4,
                    HINT * 0.4,
                    "players_four.png",
                    "players_four_hover.png",
                    game.choose_players,
                    4,
                )
                grid = Button(
                    DISP_W * 0.5,
                    HINT * 1.5,
                    HINT * 0.6,
                    HINT * 0.2,
                    "toggle_left.png",
                    "toggle_right.png",
                    game.choose_grid,
                )
                setup = Button(
                    DISP_W * 0.5,
                    HINT * 2.2,
                    HINT * 0.6,
                    HINT * 0.2,
                    "toggle_left.png",
                    "toggle_right.png",
                    game.choose_setup,
                )
                logo = Button(
                    DISP_W * 0.5,
                    HINT * 3.2,
                    HINT * 1.5,
                    HINT * 1.5,
                    "mk_logo.png",
                    "mk_logo_hover.png",
                    self._start_game,
                )
                about = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "about.png",
                    "about_hover.png",
                    self._call_about,
                )

            DIMBO_L = pygame.font.Font(
                FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.20)
            )
            DIMBO_R = pygame.font.Font(
                FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.18)
            )
            UBUNTU_R = pygame.font.Font(
                FONTS_PATH + "ubuntu_regular.ttf", int(HINT * 0.10)
            )
            UBUNTU_S = pygame.font.Font(
                FONTS_PATH + "ubuntu_regular.ttf", int(HINT * 0.05)
            )
            display.WINDOW.fill((BACKGROUND))
            blit_text(
                display.WINDOW, DIMBO_L, "Number of Players", DISP_W * 0.5, HINT * 0.3
            )
            blit_text(display.WINDOW, DIMBO_L, "Grid Size", DISP_W * 0.5, HINT * 1.2)
            blit_text(
                display.WINDOW, DIMBO_R, "5x5", DISP_W * 0.5 - HINT * 0.5, HINT * 1.5
            )
            blit_text(
                display.WINDOW, DIMBO_R, "6x6", DISP_W * 0.5 + HINT * 0.5, HINT * 1.5
            )
            blit_text(
                display.WINDOW, DIMBO_L, "Setup Variant", DISP_W * 0.5, HINT * 1.9
            )
            blit_text(
                display.WINDOW,
                DIMBO_R,
                "Standard",
                DISP_W * 0.5 - HINT * 0.7,
                HINT * 2.2,
            )
            blit_text(
                display.WINDOW,
                DIMBO_R,
                "Alternate",
                DISP_W * 0.5 + HINT * 0.7,
                HINT * 2.2,
            )

            solo.switch(display.WINDOW, (game._num_of_players == 2))
            two.switch(display.WINDOW, (game._num_of_players == 3))
            three.switch(display.WINDOW, (game._num_of_players == 4))
            four.switch(display.WINDOW, (game._num_of_players == 5))
            grid.toggle(display.WINDOW, (game._grid_size == (6, 6)), False)
            setup.toggle(display.WINDOW, (game._setup_variant == "alternate"), False)
            logo.button(display.WINDOW, False)
            about.button(display.WINDOW)

            pygame.display.update()

            for event in pygame.event.get():

                solo.get_event(display.WINDOW, event)
                two.get_event(display.WINDOW, event)
                three.get_event(display.WINDOW, event)
                four.get_event(display.WINDOW, event)
                grid.get_event(display.WINDOW, event)
                setup.get_event(display.WINDOW, event)
                logo.get_event(display.WINDOW, event)
                about.get_event(display.WINDOW, event)

                if self._about_screen:
                    self.about_screen(game, display)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)
                    self._resizing_display = True

    def game_screen(self, game, display):
        self._game_run = True
        self._resizing_display = True
        pygame.event.clear()

        while self._game_run:
            self.clock.tick(FPS)
            HINT = (
                display.HINT * 1.5
            )  # Magic number adjusts sizes without messing positions.
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H

            if self._resizing_display:
                self._resizing_display = False
                about = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "about.png",
                    "about_hover.png",
                    self._call_about,
                )

            display.WINDOW.fill((BACKGROUND))
            about.button(display.WINDOW)
            display.print_all(game.board, game.current, update=False)
            pygame.display.update()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game._abandoned = True
                    self._game_run = False

                about.get_event(display.WINDOW, event)
                if self._about_screen:
                    self.about_screen(game, display)

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)
                    self._resizing_display = True

                if game.is_end_game():
                    pygame.time.wait(1000)
                    self._game_run = False
                else:
                    if game._all_pawns_set is not True:
                        game.place_pawns(display, event)
                    if game._all_pawns_set is True:
                        game.round(display, event)
                    if game.end_turn is True:
                        game._turns += 1
                        game.change_turn()

    def end_screen(self, game, display):
        self._end_screen = True
        self._resizing_display = True
        pygame.event.clear()
        pygame.font.init()

        while self._end_screen:
            self.clock.tick(FPS)
            HINT = (
                display.HINT * 1.5
            )  # Magic number adjusts sizes without messing positions.
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H

            # BUTTON
            if self._resizing_display:
                self._resizing_display = False
                replay = Button(
                    HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "replay.png",
                    "replay_hover.png",
                    game._reset,
                )

                reveal = Button(
                    HINT * 0.5,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "reveal.png",
                    "reveal_hover.png",
                    self._call_reveal,
                )

                about = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "about.png",
                    "about_hover.png",
                    self._call_about,
                )

            if game._winner is None:
                return
            else:
                display.WINDOW.fill((BACKGROUND))

                DIMBO_L = pygame.font.Font(
                    FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.5)
                )
                DIMBO_R = pygame.font.Font(
                    FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.2)
                )
                if Player.total == 2:
                    if game._winner == game.counter:
                        blit_text(
                            display.WINDOW,
                            DIMBO_L,
                            "You Lost!",
                            DISP_W * 0.5,
                            DISP_H * 0.5 - HINT * 0.5,
                        )
                        if game._winner.score >= 6:
                            blit_text(
                                display.WINDOW,
                                DIMBO_R,
                                f"The Counter King recruited {game._winner.score} {'Pairs' if game._winner.score != 1 else 'Pair.'}",
                                DISP_W * 0.5,
                                DISP_H * 0.5 + HINT * 0.1,
                            )
                        else:
                            blit_text(
                                display.WINDOW,
                                DIMBO_R,
                                f"The Counter King reached the last card of the grid.",
                                DISP_W * 0.5,
                                DISP_H * 0.5 + HINT * 0.1,
                            )
                    else:
                        blit_text(
                            display.WINDOW,
                            DIMBO_L,
                            "You Won!",
                            DISP_W * 0.5,
                            DISP_H * 0.5 - HINT * 0.5,
                        )
                        blit_text(
                            display.WINDOW,
                            DIMBO_R,
                            f"You recruited {game._winner.score} {'Pairs' if game._winner.score != 1 else 'Pair'}.",
                            DISP_W * 0.5,
                            DISP_H * 0.5 + HINT * 0.1,
                        )
                else:
                    blit_text(
                        display.WINDOW,
                        DIMBO_L,
                        f"Player {game._winner.color} Won!",
                        DISP_W * 0.5,
                        DISP_H * 0.5 - HINT * 0.5,
                    )
                    blit_text(
                        display.WINDOW,
                        DIMBO_R,
                        f"{game._winner.score} {'Pairs' if game._winner.score != 1 else 'Pair'} Recruited.",
                        DISP_W * 0.5,
                        DISP_H * 0.5 + HINT * 0.1,
                    )

                replay.button(display.WINDOW)
                reveal.button(display.WINDOW)
                about.button(display.WINDOW)

                pygame.display.update()

                for event in pygame.event.get():

                    replay.get_event(display.WINDOW, event)
                    reveal.get_event(display.WINDOW, event)
                    about.get_event(display.WINDOW, event)

                    if event.type == pygame.QUIT:
                        self._end_screen = False

                    if event.type == pygame.VIDEORESIZE:
                        size = pygame.display.get_window_size()
                        display._resize(game.board, size)
                        self._resizing_display = True

                    if self._about_screen:
                        self.about_screen(game, display)

                    if self._reveal_cards:
                        self.reveal_cards(game, display)

    def reveal_cards(self, game, display):
        self._reveal_cards = True
        self._resizing_display = True
        pygame.event.clear()
        pygame.font.init()

        while self._reveal_cards:
            self.clock.tick(FPS)
            HINT = (
                display.HINT * 1.5
            )  # Magic number adjusts sizes without messing positions.
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H

            if self._resizing_display:
                self._resizing_display = False
                replay = Button(
                    HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "replay.png",
                    "replay_hover.png",
                    game._reset,
                )

                reveal = Button(
                    HINT * 0.5,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "reveal.png",
                    "reveal_hover.png",
                    self._call_reveal,
                )

                about = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "about.png",
                    "about_hover.png",
                    self._call_about,
                )

            display.WINDOW.fill((BACKGROUND))
            about.button(display.WINDOW)
            replay.button(display.WINDOW)
            reveal.button(display.WINDOW)
            display.print_all(
                game.board,
                current_player=None,
                invalid_moves=False,
                grid_revealed=True,
                update=False,
            )
            pygame.display.update()

            for event in pygame.event.get():

                about.get_event(display.WINDOW, event)
                reveal.get_event(display.WINDOW, event)
                replay.get_event(display.WINDOW, event)

                if self._about_screen:
                    self.about_screen(game, display)

                if game._reset_game:
                    self._reveal_cards = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)
                    self._resizing_display = True

    def about_screen(self, game, display):
        pygame.event.clear()
        pygame.font.init()

        while self._about_screen:
            self.clock.tick(FPS)
            self._resizing_display = True
            HINT = (
                display.HINT * 1.5
            )  # Magic number adjusts sizes without messing positions.
            DISP_W = display.DISP_W
            DISP_H = display.DISP_H

            if self._resizing_display:
                self._reisizing_display = False
                pdf_logo = Button(
                    DISP_W * 0.5 - HINT,
                    HINT * 1.5,
                    HINT * 0.4,
                    HINT * 0.4,
                    "pdf_logo.png",
                    action_func=self._open_link,
                    action_arg="https://drive.google.com/file/d/1be3mYSzGpOooiSTmYnRBguKZ-2J40ip9/view?usp=sharing",
                )

                youtube_logo = Button(
                    DISP_W * 0.5 + HINT,
                    HINT * 1.5,
                    HINT * 0.4,
                    HINT * 0.4,
                    "youtube_logo.png",
                    action_func=self._open_link,
                    action_arg="https://youtu.be/snqjQtYmv_Q",
                )

                bgg_logo = Button(
                    DISP_W * 0.5,
                    HINT * 2.8,
                    HINT * 0.4,
                    HINT * 0.4,
                    "bgg_logo.png",
                    action_func=self._open_link,
                    action_arg="https://boardgamegeek.com/boardgame/319384/memory-kings",
                )
                tgc_logo = Button(
                    DISP_W * 0.5 - HINT * 0.8,
                    HINT * 2.6,
                    HINT * 0.4,
                    HINT * 0.4,
                    "tgc_logo.png",
                    action_func=self._open_link,
                    action_arg="https://www.thegamecrafter.com/games/memory-kings",
                )
                facebook_logo = Button(
                    DISP_W * 0.5 + HINT * 0.8,
                    HINT * 2.6,
                    HINT * 0.4,
                    HINT * 0.4,
                    "facebook_logo.png",
                    action_func=self._open_link,
                    action_arg="https://www.facebook.com/memorykingsthegame",
                )
                sneaky_pirates_logo = Button(
                    DISP_W * 0.5,
                    DISP_H - HINT * 0.6,
                    HINT * 0.6,
                    HINT * 0.6,
                    "sneaky_pirates_logo.png",
                )
                mute = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.49,
                    HINT * 0.2,
                    HINT * 0.2,
                    "sound_on.png",
                    "sound_off.png",
                    self._mute,
                )
                about = Button(
                    DISP_W - HINT * 0.2,
                    DISP_H - HINT * 0.19,
                    HINT * 0.2,
                    HINT * 0.2,
                    "about.png",
                    "about_hover.png",
                    self._call_about,
                )

            display.WINDOW.fill((BACKGROUND))
            DIMBO_L = pygame.font.Font(
                FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.20)
            )
            DIMBO_R = pygame.font.Font(
                FONTS_PATH + "dimbo_regular.ttf", int(HINT * 0.12)
            )
            UBUNTU_R = pygame.font.Font(
                FONTS_PATH + "ubuntu_regular.ttf", int(HINT * 0.10)
            )
            UBUNTU_S = pygame.font.Font(
                FONTS_PATH + "ubuntu_regular.ttf", int(HINT * 0.05)
            )
            blit_text(display.WINDOW, DIMBO_L, "About", DISP_W * 0.5, HINT * 0.3)
            blit_long_text(
                display.WINDOW,
                "In Memory Kings, players challenge their memory in a mix of the classic games of Chess and Pairs (a.k.a. memory®). They move their pawns strategically across a grid of hidden cards, revealing them, and finding indentical pairs. The player that finds the most pairs wins!",
                (HINT * 0.5, HINT * 0.5),
                UBUNTU_R,
                HINT * 0.5,
            )
            blit_text(display.WINDOW, DIMBO_L, "How to Play", DISP_W * 0.5, HINT * 1.6)
            blit_text(
                display.WINDOW,
                DIMBO_R,
                "Official Rulebook",
                DISP_W * 0.5 - HINT,
                HINT * 1.89,
            )
            blit_text(
                display.WINDOW,
                DIMBO_R,
                "Video Tutorial",
                DISP_W * 0.5 + HINT,
                HINT * 1.81,
            )
            blit_text(
                display.WINDOW,
                DIMBO_R,
                " (2-4 Players)",
                DISP_W * 0.5 + HINT,
                HINT * 1.97,
            )
            blit_text(display.WINDOW, DIMBO_L, "Links", DISP_W * 0.5, HINT * 2.4)
            blit_text(
                display.WINDOW,
                DIMBO_R,
                "Digital Version by G. Scary T.",
                DISP_W * 0.5,
                DISP_H - HINT * 0.2,
            )
            blit_text(
                display.WINDOW,
                UBUNTU_S,
                "Memory Kings v0.7 in Python 3.8 (Alpha)",
                DISP_W * 0.01,
                DISP_H * 0.99,
                "bottomleft",
            )

            mute.toggle(display.WINDOW, (Asset._mute_sounds == True))
            about.button(display.WINDOW)
            pdf_logo.button(display.WINDOW)
            youtube_logo.button(display.WINDOW)
            bgg_logo.button(display.WINDOW)
            tgc_logo.button(display.WINDOW)
            facebook_logo.button(display.WINDOW)
            sneaky_pirates_logo.button(display.WINDOW, False)

            pygame.display.update()

            for event in pygame.event.get():

                mute.get_event(display.WINDOW, event)
                about.get_event(display.WINDOW, event)
                pdf_logo.get_event(display.WINDOW, event)
                youtube_logo.get_event(display.WINDOW, event)
                bgg_logo.get_event(display.WINDOW, event)
                tgc_logo.get_event(display.WINDOW, event)
                facebook_logo.get_event(display.WINDOW, event)
                sneaky_pirates_logo.get_event(display.WINDOW, event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(game.board, size)
                    self._resizing_display = True

    # TRANSITION METHODS

    def _start_game(self):
        self._start_menu = False

    def _call_about(self):
        if self._about_screen is False:
            self._about_screen = True
        else:
            self._about_screen = False

    def _open_link(self, link):
        import webbrowser

        webbrowser.open_new_tab(link)

    def _call_reveal(self):
        if self._reveal_cards is False:
            self._reveal_cards = True
        else:
            self._reveal_cards = False

    def _mute(self):
        if Asset._mute_sounds is False:
            Asset._mute_sounds = True
        else:
            Asset._mute_sounds = False

# UTILITARY FUNCTIONS


def blit_text(surface, font, text_input, x, y, relative_to="center", color=WHITE):
    text = font.render(text_input, True, color)
    text_rect = text.get_rect()
    if relative_to == "center":
        text_rect.center = (int(x), int(y))
    elif relative_to == "topright":
        text_rect.topright = (int(x), int(y))
    elif relative_to == "topleft":
        text_rect.topleft = (int(x), int(y))
    elif relative_to == "bottomright":
        text_rect.bottomright = (int(x), int(y))
    elif relative_to == "bottomleft":
        text_rect.bottomleft = (int(x), int(y))
    else:
        text_rect.center = (int(x), int(y))
    surface.blit(text, text_rect)


def blit_image(surface, image, pos, width, height):
    loaded = pygame.image.load(IMAGES_PATH + image).convert_alpha()
    scaled = pygame.transform.scale(loaded, (int(width), int(height)))
    rect = scaled.get_rect()
    x, y = pos
    rect.center = (x, y)
    surface.blit(scaled, rect)


def blit_long_text(surface, text, pos, font, x_padding=0, color=WHITE):
    """
    Adapted from Ted Klein Bergman on StackOverflow.
    """
    words = [
        word.split(" ") for word in text.splitlines()
    ]  # 2D array where each row is a list of words.
    space = font.size(" ")[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width - x_padding:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height


def blit_FPS(clock, display):
    HINT = display.HINT * 1.5  # Magic number adjusts sizes without messing positions.
    DISP_W = display.DISP_W
    DISP_H = display.DISP_H
    UBUNTU_S = pygame.font.Font(FONTS_PATH + "ubuntu_regular.ttf", int(HINT * 0.05))
    blit_text(
        display.WINDOW,
        UBUNTU_S,
        str(clock.get_fps()),
        DISP_W * 0.01,
        DISP_H * 0.99,
        relative_to="bottomleft",
    )
    pygame.display.update()
