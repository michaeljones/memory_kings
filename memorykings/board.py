import pygame, random, time
from .constants import COLORS, RANKS, BACKS, CARD_SIZE, CORNER

import logging as log
log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
log.disable(log.CRITICAL)

### BOARD ###

class Board:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.width = self.cols*CARD_SIZE
        self.height = self.rows*CARD_SIZE
        self.grid = [] # REDUNDANT FOR NOW... NOT SURE IF NEEDED.

    def gen_grid(self):
        Queen("", "QUEEN", "BLACK") # Generate the Queen Card first.
        for _, back in enumerate(BACKS):
            for _, color in enumerate(COLORS[: 4]): # Colors = (cols*rows - special_cards)/(backs*ranks)
                for _, rank in enumerate(RANKS):
                    if rank == "BISHOP":
                        Bishop(color, rank, back)
                    elif rank == "ROOK":
                        Rook(color, rank, back)
                    elif rank == "KNIGHT":
                        Knight(color, rank, back)
        random.shuffle(Card.deck)
        for i, _ in enumerate(Card.deck):
            Card.deck[i].position = i
            Card.deck[i].col = i % self.cols
            Card.deck[i].row = i // self.cols
        self.grid = Card.deck[i:self.cols*(1+i)] # REDUNDANT FOR NOW... NOT SURE IF NEEDED

    def get_card(self, col, row):
        return self.grid[col][row]

    def click_to_grid(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        click_pos = [0, 0]
        if click[0] == 1:
            if not (mouse[0] < CORNER[0] or mouse[1] < CORNER[1] 
                or mouse[0] > CORNER[0]+self.rows*CARD_SIZE
                or mouse[1] > CORNER[1]+self.cols*CARD_SIZE):
                for i in range(self.rows):
                    if i < (mouse[0]-150)/CARD_SIZE and (mouse[0]-150-CARD_SIZE)/CARD_SIZE < i:
                        click_pos[0] = i
                for j in range(self.cols):
                    if j < (mouse[1]-50)/CARD_SIZE and (mouse[1]-50-CARD_SIZE)/CARD_SIZE < j:
                        click_pos[1] = j
                log.debug(f'click_to_grid() - Mouse click on {mouse} represents the {click_pos} coordinates.')
                return click_pos
            else:
                log.debug(f'click_to_grid() - Mouse click outside the board.')
                return None


### CARDS ###

class Card:
    deck = []
    def __init__(self, color, rank, back):
        self.color = color
        self.rank = rank
        self.back = back
        self.image = color + '_' + rank + '.png'
        self.recruited = None
        self.position = 0
        self.col = 0
        self.row = 0
        Card.deck.append(self)

    def is_token(self, token_array):
        for token in token_array:
            if (token.position == self.position):
                return token.color
        return None

    def escort_token_check(self, pawn, token_array, col, row):
        log.debug(f'escort_token_check() - Is token {self.is_token(token_array)} on {self.position}. Pawn position: {pawn.position}')
        if (self.is_token(token_array) != None
        and self.is_token(token_array) != pawn.color):
            log.debug(f"escort_token_check() - There is an Opponent's Token on Card {self.position}")
            return True

    def activate(self, player_array):
        for player in player_array:
            for pawn in player.pawn:
                for token in player.token:
                    if token.position == self.position:
                        return False
                if pawn.previous == self.position:
                    return False
        return True

    def special(self, window, display, board, player_array, event):
        pass

class Bishop(Card):
    def escort_check(self, pawn, token_array, col, row):
        if not self.escort_token_check(pawn,token_array,col,row):
            if abs(col - self.col) == abs(row - self.row):
                log.debug(f"escort_check() - Valid Bishop Escort."
                f" {self.col}, {self.row} >> {col}, {row}")
                return True
            else:
                log.debug(f"escort_check() - The Bishop cannot Escort to {col}, {row}.")
                return False
        else:
            return False

class Rook(Card):
    def escort_check(self, pawn, token_array, col, row):
        if self.escort_token_check(pawn,token_array,col,row):
            return False
        else:
            if col == self.col or row == self.row:
                log.debug(f"escort_check() - Valid Rook Escort."
                f" {self.col}, {self.row} >> {col}, {row}")
                return True
            else:
                log.debug(f"escort_check() - The Rook cannot Escort to {col}, {row}.")
                return False

class Knight(Card):
    def escort_check(self, pawn, token_array, col, row):
        if not self.escort_token_check(pawn,token_array,col,row):
            if (
                (abs(col-self.col) == 2 and abs(row-self.row) == 1) 
                or (abs(col-self.col) == 1 and abs(row-self.row) == 2)
                ):
                log.debug(f"escort_check() - Valid Knight Escort."
                f" {self.col}, {self.row} >> {col}, {row}")
                return True
            else:
                log.debug(f"escort_check() - The Knight cannot Escort to {col}, {row}.")
                return False
        else:
            return False

class Queen(Card):
    def escort_check(self, pawn, token_array, col, row):
        if not self.escort_token_check(pawn,token_array,col,row):
            if (
                (abs(col - self.col) == abs(row - self.row))
                or ((col == self.col) or (row == self.row))
                ):
                log.debug(f"escort_check() - Valid Queen Escort."
                f" {self.col}, {self.row} >> {col}, {row}")
                return True
            else:
                log.debug(f"escort_check() - The Queen cannot Escort to {col}, {row}.")
                return False
        else:
            return False

    def special(self, window, display, board, player_array, event):
        if self.activate(player_array):
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = board.click_to_grid()
                card = board.get_card(click_pos[0], click_pos[1])
                coords_on_screen = CORNER[0]+CARD_SIZE*card.col, CORNER[1]+CARD_SIZE*card.row
                card_image = display.get_image(card.image, CARD_SIZE, CARD_SIZE)
                window.blit(card_image, coords_on_screen)
                pygame.display.update()
                time.sleep(1)