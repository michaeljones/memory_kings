import pygame
import sys
from .buttons import Button
from .constants import BACKGROUND, FPS
from .assets import sound


class Card:
    array = []
    queen_uses = 0

    def __init__(self, color, rank, back):
        self.color = color
        self.rank = rank
        self.back = back
        self.image = color.lower() + "_" + rank.lower() + ".png"

        self.col = 0  # Position col,row is redefined on Board Grid Setup
        self.row = 0
        self.remember = False

        Card.array.append(self)

    @property
    def position(self):
        return (self.col, self.row)

    def is_valid_escort(self, col, row):
        """
        Generic cards cannot escort.
        """
        return False

    def activate(self, player_array, col, row):
        """
        Check if a card was hidden or open when a pawn moves
        to it. Special powers (like the Queen's Peeking Card) only
        activate when a card is flipped from facing down to up.
        """
        for player in player_array:
            for pawn in player.pawn:
                if pawn.previous == self.position:
                    return False
            for token in player.token:
                if token.position == self.position:
                    return False
        return True

    def special(self, *args):
        """Standard Cards have no special effects."""
        pass


class Bishop(Card):
    def is_valid_escort(self, col, row):
        """
        Checks if the destination is on a diagonal from the card.
        1) col: Destination column.
        2) row: Destination row.
        """
        if abs(col - self.col) == abs(row - self.row):
            return True
        else:
            return False


class Rook(Card):
    def is_valid_escort(self, col, row):
        """
        Checks if the destination is orthogonal from the card.
        1) col: Destination column.
        2) row: Destination row.
        """
        if col == self.col or row == self.row:
            return True
        else:
            return False


class Knight(Card):
    def is_valid_escort(self, col, row):
        """
        Checks if the destination is on a "L" pattern from the card.
        1) col: Destination column.
        2) row: Destination row.
        """
        if (abs(col - self.col) == 2 and abs(row - self.row) == 1) or (
            abs(col - self.col) == 1 and abs(row - self.row) == 2
        ):
            return True
        else:
            return False


class Queen(Card):
    def is_valid_escort(self, col, row):
        """
        Checks if the destination is orthogonal or diagonal from the card.
        1) col: Destination column.
        2) row: Destination row.
        """
        if (
            (abs(col - self.col) == abs(row - self.row))
            or (col == self.col)
            or (row == self.row)
        ):
            return True
        else:
            return False

    def special(self, display, board):
        """
        When the Queen is activated, the Player can
        peek any hidden card from the board.
        """
        clock = pygame.time.Clock()
        sound("queen.wav")
        while True:
            clock.tick(FPS)
            display.get_cursor_eye()
            display.WINDOW.fill((BACKGROUND))
            display.print_all(board, update="off", invalid_moves="off")
            display.print_eye(board, self.col, self.row)
            locked1 = Button(
                display.HINT * 0.3,
                display.DISP_H - display.HINT * 0.285,
                display.HINT * 0.3,
                display.HINT * 0.3,
                "button_locked.png",
            )
            locked2 = Button(
                display.DISP_W - display.HINT * 0.3,
                display.DISP_H - display.HINT * 0.285,
                display.HINT * 0.3,
                display.HINT * 0.3,
                "button_locked.png",
            )
            locked1.button(display.WINDOW, False)
            locked2.button(display.WINDOW, False)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    display._resize(board, size)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = board.get_click_to_pos(display, event)
                    if click_pos is not None:
                        if not display.print_card(board, click_pos[0], click_pos[1]):
                            continue
                        else:
                            Card.queen_uses += 1
                            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                            return True
