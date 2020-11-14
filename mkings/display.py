import pygame
from .constants import (IMAGES_PATH,PLAYER_COLOR_CODES)
from .players import Player
from .pawns import Pawn

class Display:
    def __init__(self, HINT=100):
        self._original_HINT=HINT
        self._init(HINT)
    
    def _init(self, HINT):
        self.HINT = int(HINT)
        self.DISP_W = int(HINT*6.00)
        self.DISP_H = int(HINT*6.50)
        self.CARD_SIZE = int(HINT)
        self.CARD_BORDER = int(HINT*0.05)
        self.TOKEN_SIZE = int(HINT*0.20)
        self.PAWN_SIZE = int(HINT*0.20)
        self.CORNER = int(0),int(0)
        self.WINDOW = pygame.display.set_mode((self.DISP_W, self.DISP_H), pygame.RESIZABLE)
        pygame.display.set_caption("Memory Kings")
    
    def _resize(self, board, size):
        if size[0] != self.DISP_W:
            NEW_HINT = self._original_HINT*size[0]/650
        elif size[1] != self.DISP_H:
            NEW_HINT = self._original_HINT*size[1]/600
        self._init(NEW_HINT)
        self._set_corner(board)

    def _set_corner(self,board):
        try:
            self.CORNER = (
                int((self.DISP_W - self.CARD_SIZE*board.cols)/2), 
                int((self.DISP_W - self.CARD_SIZE*board.rows)/2),
                )
        except Exception:
            self.CORNER = (0,0)

    def get_image(self, image, width, height):
        """Loads and returns an image with the given size"""
        return pygame.transform.scale(
            pygame.image.load(IMAGES_PATH + image).convert_alpha(), (width, height)
        )

    def print_grid(self, board):
        """
        Prints the board (grid of cards). Prints the face of any
        card with a token or a pawn on it and the back of any other
        """
        for row in range(board.rows):
            for col in range(board.cols):
                card = board.get_card(row, col)
                pos_on_screen = (
                    self.CORNER[0] + self.CARD_SIZE * card.col,
                    self.CORNER[1] + self.CARD_SIZE * card.row,
                )
                is_open = False

                for player in Player.array:
                    for pawn in player.pawn:
                        if pawn.position == card.position:
                            card_image = self.get_image(card.image, self.CARD_SIZE, self.CARD_SIZE)
                            self.WINDOW.blit(card_image, pos_on_screen)
                            is_open = True
                    for token in player.token:
                        if token.position == card.position:
                            card_image = self.get_image(
                                card.image, self.CARD_SIZE, self.CARD_SIZE
                            )
                            self.WINDOW.blit(card_image, pos_on_screen)
                            is_open = True

                if not is_open:
                    if card.back == "WHITE":
                        white_back = self.get_image("white_back.png", self.CARD_SIZE, self.CARD_SIZE)
                        self.WINDOW.blit(white_back, pos_on_screen)
                    elif card.back == "BLACK":
                        black_back = self.get_image("black_back.png", self.CARD_SIZE, self.CARD_SIZE)
                        self.WINDOW.blit(black_back, pos_on_screen)

    def print_pawns(self):
        """Gets and prints all placed pawns of all players"""
        for player in Player.array:
            for pawn in player.pawn:
                pos_on_screen = player._get_pawn_on_screen(self, pawn)
                pawn_image = self.get_image(
                    pawn.image, self.PAWN_SIZE, self.PAWN_SIZE
                )
                self.WINDOW.blit(pawn_image, pos_on_screen)
    
    def print_tokens(self):
        """Gets and prints all placed tokens of all players"""
        for player in Player.array:
            for token in player.token:
                pos_on_screen = (
                    int((self.CORNER[0] + self.CARD_SIZE * (1 + token.col))-7*self.TOKEN_SIZE//6),
                    int((self.CORNER[1] + self.CARD_SIZE * (token.row))+self.TOKEN_SIZE//5),
                )
                token_image = self.get_image(token.image, self.TOKEN_SIZE, self.TOKEN_SIZE)
                self.WINDOW.blit(token_image, pos_on_screen)

    def print_selected(self, current_player):
        """Prints a small highlight under the selected pawn."""
        if Pawn.selected:
            pos_on_screen = list(current_player._get_pawn_on_screen(self, Pawn.selected))
            pos_on_screen[0] -= self.PAWN_SIZE//5
            pos_on_screen[1] -= self.PAWN_SIZE//5
            pawn_image = self.get_image(
                "selected_shadow.png", 7*self.PAWN_SIZE//5, 7*self.PAWN_SIZE//5
            )
            self.WINDOW.blit(pawn_image, pos_on_screen)
    
    def print_invalid_moves(self, board):
        """
        Prints a "deny" sign over any card that can't be reached
        by the selected pawn
        """
        if Pawn.selected:
            for rows in board.grid:
                for card in rows:
                    pos_on_screen = (
                        self.CORNER[0] + self.CARD_SIZE * card.col,
                        self.CORNER[1] + self.CARD_SIZE * card.row,
                    )
                    if not Pawn.selected.check_move(
                        board, Player, card.col, card.row
                    ):
                        if card.position == Pawn.selected.position:
                            continue
                        else:
                            image = self.get_image("unavailable.png", self.CARD_SIZE, self.CARD_SIZE)
                            self.WINDOW.blit(image, pos_on_screen)

    def print_score_board(self):
        pygame.font.init()
        DIMBO_L = pygame.font.Font("fonts/dimbo_regular.ttf", self.CARD_SIZE//5)
        for i, player in enumerate(Player.array):
            t1 = DIMBO_L.render(f"{player.color}: {player.score}", True, PLAYER_COLOR_CODES[i])
            t1_rect = t1.get_rect()
            if Player.total == 2:
                t1_rect.center = (
                    (self.DISP_W*0.5) - (self.CARD_SIZE*0.5) + (i * self.CARD_SIZE),
                    self.DISP_H - self.HINT//4 - self.CORNER[1],
                )
                self.WINDOW.blit(t1, t1_rect)
            else:
                if i != 0:
                    if Player.total == 3:
                        t1_rect.center = (
                            (self.DISP_W*0.5) - (self.CARD_SIZE*0.5) + ((i - 1) * self.CARD_SIZE),
                            self.DISP_H - self.HINT//4 - self.CORNER[1],
                        )
                        self.WINDOW.blit(t1, t1_rect)
                    elif Player.total == 4:
                        t1_rect.center = (
                            (self.DISP_W*0.5) - (self.CARD_SIZE) + ((i - 1) * self.CARD_SIZE),
                            self.DISP_H - self.HINT//4 - self.CORNER[1],
                        )
                        self.WINDOW.blit(t1, t1_rect)
                    else:
                        t1_rect.center = (
                            (self.DISP_W*0.5) - (3 * self.CARD_SIZE*0.5) + ((i - 1) * self.CARD_SIZE),
                            self.DISP_H - self.HINT//4 - self.CORNER[1],
                        )
                        self.WINDOW.blit(t1, t1_rect)
        pygame.display.update()

    def print_all(self, board, current_player):
        """
        Print all layers of the game in the order:
        grid > select pawn highlight > valid_moves > pawns > tokens
        """
        self.print_grid(board)
        self.print_selected(current_player)
        self.print_invalid_moves(board)
        self.print_pawns()
        self.print_tokens()
        self.print_score_board()
        pygame.display.update()

    def print_card(self, board, col, row):
        """Show one hidden card for 2 seconds and turns it back down."""
        card = board.get_card(col,row)
        pos_on_screen = (
            self.CORNER[0] + self.CARD_SIZE * col,
            self.CORNER[1] + self.CARD_SIZE * row,
        )
        is_open = False
        for player in Player.array:
            for pawn in player.pawn:
                if pawn.position == card.position:
                    is_open = True
                    return False
            for token in player.token:
                if token.position == card.position:
                    is_open = True
                    return False
        if not is_open:
            card_image = self.get_image(card.image, self.CARD_SIZE, self.CARD_SIZE)
            self.WINDOW.blit(card_image, pos_on_screen)
            pygame.display.update()
            pygame.time.wait(2000)
            return True