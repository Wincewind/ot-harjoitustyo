import pygame
from ui.gamesprites import GameSprites
import ui.instructions
import config


class Renderer:
    def __init__(self, display: pygame.display, game_sprites: GameSprites):
        self._display = display
        self._game_sprites = game_sprites
        self.winner = 0

    def render(self):
        self._display.fill(config.BOARD_COLOR)
        self._game_sprites.clear_caravan_area()
        if self._game_sprites.player_turn is not None:
            self._game_sprites.update_hand_sprites()
        ui.instructions.write_game_controls(self._display)
        # if self._game_sprites.chosen_crd_sprite is not None:
        #     self._game_sprites.update_caravan_sprites()
        # if self._game_sprites.player_turn:
        # self._game_sprites.player_sprites.draw(self._display)
        # self._hand_sel.update_hand_sprites()
        self._game_sprites.update_all_sprites()
        self._game_sprites.all.draw(self._display)
        if self.winner != 0:
            ui.instructions.game_over_message(self.winner, self._display)
        pygame.display.update()
