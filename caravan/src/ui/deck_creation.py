import pygame
import config
from repositories.player_data_repository import player_data_repository, DataNotFoundException
from ui.eventqueue import EventQueue
from entities.player_data import PlayerData


class DeckCreation:
    """A class for the deck creation UI. Currently only card set selection is available as an option.

    Attributes:
        pl_data: PlayerData object containing the information about player's available card sets.
    """
    def __init__(self, display, event_queue, player_data: PlayerData):
        pygame.display.set_caption("Deck Selection")
        self._display = display
        self._display.fill(config.BOARD_COLOR)
        self._event_queue = event_queue
        self.pl_data = player_data
        self._available_sets = player_data.card_sets+['All']
        self._user_selection = None
        self._set_rects_info = [0, 0, 0]
        self._update_set_selection_rects()
        self._draw_screen()

    def _update_set_selection_rects(self):
        font_color = (0, 0, 0)
        text = config.BIG_FONT.render(
            'Select a set to create your deck from:', True, font_color)
        text_y = 100
        text_x = config.BOARD_WIDTH/2-text.get_width()/2
        rect = pygame.Rect(text_x-50, text_y-50,
                           text.get_width()+100, text.get_height()+100)
        self._draw_rect_and_text(
            config.BOARD_COLOR, rect, text, (text_x, text_y))
        text_y += 200
        for i in range(3):
            txt = self._available_sets[i]
            text = config.BIG_FONT.render(txt, True, font_color)
            text_x = config.BOARD_WIDTH/2-text.get_width()/2
            rect = pygame.Rect(text_x-50, text_y-50,
                               text.get_width()+100, text.get_height()+100)
            rect_col = (192, 192, 192)
            if i == self._user_selection:
                rect_col = (
                    config.OVERLAY_YELLOW[0], config.OVERLAY_YELLOW[1], config.OVERLAY_YELLOW[2])
            info = {'text': text, 'text_xy': (
                text_x, text_y), 'rect_col': rect_col, 'rect': rect}
            self._set_rects_info[i] = info
            text_y += 200

    def _draw_rect_and_text(self, rect_col, rect, text, text_xy):
        pygame.draw.rect(self._display,
                         rect_col,
                         rect,
                         border_radius=3)
        self._display.blit(text, text_xy)

    def _draw_screen(self):
        for i in range(3):
            self._draw_rect_and_text(
                self._set_rects_info[i]['rect_col'],
                self._set_rects_info[i]['rect'],
                self._set_rects_info[i]['text'],
                self._set_rects_info[i]['text_xy'])
        pygame.display.update()

    def main_loop(self):
        """Loop to handle the user inputs regarding what card set they want to use to create their deck.

        Returns:
            Player: Once a card set is chosen, it's used to create a 
            deck and a Player object is prepared using this. if the UI is quit, None is returned.
        """
        while True:
            for event in self._event_queue.get():
                self._user_selection = None
                for i, info in enumerate(self._set_rects_info):
                    if info['rect'].collidepoint(pygame.mouse.get_pos()):
                        self._user_selection = i
                        break
                self._update_set_selection_rects()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self._user_selection in range(len(self._available_sets)):
                        return self.pl_data.prepare_player(self._available_sets[self._user_selection])

                if event.type == pygame.QUIT:
                    return None
                self._draw_screen()
