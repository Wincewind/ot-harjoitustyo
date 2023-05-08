import pygame
from ui.gamesprites import GameSprites
import ui.instructions
import config


class Renderer:
    """Class that renders the Caravan gamescreen 
    sprites and a message once one of the players have won.

    Attributes:
        winner (int): winning player's number, either 1 or 2 that's used in the 
        message to congratulate the winner. If the game is not over, the value is 0.
    """
    def __init__(self, display: pygame.display, game_sprites: GameSprites):
        self._display = display
        self._game_sprites = game_sprites
        self.winner = 0

    def render(self):
        """Draw game sprites onto pygame display and update it.
        """
        self._display.fill(config.BOARD_COLOR)
        self._game_sprites.clear_caravan_area()
        if self._game_sprites.player_turn is not None:
            self._game_sprites.update_hand_sprites()
        ui.instructions.write_game_controls(self._display)
        self._game_sprites.update_all_sprites()
        self._game_sprites.all.draw(self._display)
        if self.winner != 0:
            ui.instructions.game_over_message(self.winner, self._display)
        pygame.display.update()
