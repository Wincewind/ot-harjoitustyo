import pygame
import config
from repositories.player_data_repository import player_data_repository


class SaveSelection:
    """A class for the save selection and deletion UI.
    """
    def __init__(self, display, event_queue):
        pygame.display.set_caption("Save Selection")
        self._display = display
        self._event_queue = event_queue
        self._existing_saves = None
        self._init_existing_saves()
        self._existing_saves = player_data_repository.find_all_player_names()
        self._user_selection = None
        self._user_action = None
        self._save_slot_information = [0, 0, 0]
        self._select_delete_rects = [0, 0]
        self._save_selected = False
        self._update_save_slot_rects()
        self._update_select_and_delete_rects()

    def _init_existing_saves(self):
        self._existing_saves = player_data_repository.find_all_player_names()

    def _update_select_and_delete_rects(self):
        for i, action in enumerate([
            {'text': 'Select', 'text_x': 100},
                {'text': 'Delete', 'text_x': config.BOARD_WIDTH-200}]):
            font_color = (0, 0, 0)
            text = config.MED_FONT.render(action['text'], True, font_color)
            text_y = config.BOARD_HEIGHT-200
            text_x = action['text_x']
            rect = pygame.Rect(text_x-50, text_y-50,
                               text.get_width()+100, text.get_height()+100)
            rect_col = (192, 192, 192)
            if action['text'] == self._user_action:
                rect_col = (
                    config.OVERLAY_YELLOW[0], config.OVERLAY_YELLOW[1], config.OVERLAY_YELLOW[2])
            self._select_delete_rects[i] = {'action': action['text'], 'text': text, 'text_xy': (text_x, text_y),
                                           'rect_col': rect_col, 'rect': rect}

    def _update_save_slot_rects(self, user_input=None):
        font_color = (0, 0, 0)
        text = config.BIG_FONT.render('Create a new save', True, font_color)
        text_y = config.BOARD_HEIGHT/3-text.get_height()
        for i in range(3):
            if user_input is not None and self._user_selection == i:
                msg = user_input
            elif i not in self._existing_saves:
                msg = 'Create a new save'
            else:
                msg = self._existing_saves[i]['name']
                msg += f" - W: {self._existing_saves[i]['wins']} L: {self._existing_saves[i]['losses']}"
            text = config.BIG_FONT.render(msg, True, font_color)
            text_x = config.BOARD_WIDTH/2-text.get_width()/2
            rect = pygame.Rect(text_x-50, text_y-50,
                               text.get_width()+100, text.get_height()+100)
            rect_col = (192, 192, 192)
            if i == self._user_selection:
                rect_col = (
                    config.OVERLAY_YELLOW[0], config.OVERLAY_YELLOW[1], config.OVERLAY_YELLOW[2])
            info = {'text': text, 'text_xy': (
                text_x, text_y), 'rect_col': rect_col, 'rect': rect}
            self._save_slot_information[i] = info
            text_y += 200

    def _draw_rect_and_text(self, rect_col, rect, text, text_xy):
        pygame.draw.rect(self._display,
                         rect_col,
                         rect,
                         border_radius=3)
        self._display.blit(text, text_xy)

    def _draw_screen(self):
        self._display.fill(config.BOARD_COLOR)
        for i in range(3):
            self._draw_rect_and_text(
                self._save_slot_information[i]['rect_col'],
                self._save_slot_information[i]['rect'],
                self._save_slot_information[i]['text'],
                self._save_slot_information[i]['text_xy'])
        for i in range(2):
            self._draw_rect_and_text(
                self._select_delete_rects[i]['rect_col'],
                self._select_delete_rects[i]['rect'],
                self._select_delete_rects[i]['text'],
                self._select_delete_rects[i]['text_xy'])
        pygame.display.update()

    def _get_user_input(self):
        user_input = ''
        self._update_save_slot_rects(user_input)
        self._draw_screen()
        while True:
            for event in self._event_queue.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        player_data_repository.create_player_data(
                            user_input, self._user_selection)
                        self._init_existing_saves()
                        return True
                    else:
                        user_input += event.unicode
                    self._update_save_slot_rects(user_input)
                    self._draw_screen()

    def _reset_save_selection(self):
        self._save_selected = False
        self._user_selection = None
        self._user_action = None
        self._update_select_and_delete_rects()
        self._init_existing_saves()

    def _check_for_action(self):
        while True:
            self._user_action = None
            for i, info in enumerate(self._select_delete_rects):
                if info['rect'].collidepoint(pygame.mouse.get_pos()):
                    self._user_action = info['action']
                    break

            for event in self._event_queue.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self._reset_save_selection()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN and self._user_action is not None:
                    if self._user_action == 'Select':
                        return True
                    if self._user_action == 'Delete':
                        player_data_repository.delete_player_data(
                            self._existing_saves[self._user_selection]['name'],self._user_selection)
                        self._reset_save_selection()
                        return None

            self._update_select_and_delete_rects()
            self._draw_screen()

    def main_loop(self):
        """Loop to handle the user inputs regarding what save 
        slot to select, what name to give the player data and if the data in 
        the slot should be proceeded with or deleted.

        Returns:
            PlayerData: PlayerData object of the chosen save. If the UI is quit, None is returned instead.
        """
        while True:
            for event in self._event_queue.get():
                self._user_selection = None
                for i, info in enumerate(self._save_slot_information):
                    if info['rect'].collidepoint(pygame.mouse.get_pos()):
                        self._user_selection = i
                        break
                self._update_save_slot_rects()

                if event.type == pygame.MOUSEBUTTONDOWN and self._user_selection in self._existing_saves:
                    result = self._check_for_action()
                    if result is False:
                        return None
                    if result is True:
                        return player_data_repository.find_player_data(
                            self._existing_saves[self._user_selection]['name'],self._user_selection)
                elif event.type == pygame.MOUSEBUTTONDOWN and self._user_selection is not None and not self._get_user_input():
                    return None

                if event.type == pygame.QUIT:
                    return None
                self._draw_screen()
