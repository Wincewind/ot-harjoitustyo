import pygame
import config
from repositories.player_data_repository import player_data_repository, DataNotFoundException
from ui.eventqueue import EventQueue

class SaveSelection:
    def __init__(self, display, event_queue):
        pygame.display.set_caption("Save Selection")
        self._display = display
        self._event_queue = event_queue
        self._existing_saves = player_data_repository.find_all_player_names()
        self._user_selection = None
        self.save_slot_information = [0,0,0]
        self._update_save_slot_rects()

    def _update_save_slot_rects(self,user_input=None):
        font_color = (0, 0, 0)
        text = config.BIG_FONT.render('Create a new save', True, font_color)
        text_y = config.BOARD_HEIGHT/3-text.get_height()
        for i in range(3):
            if user_input is not None and self._user_selection == i:
                msg = user_input
            elif i not in self._existing_saves:
                msg = 'Create a new save'
            else:
                msg = self._existing_saves[i]
            text = config.BIG_FONT.render(msg, True, font_color)
            text_x = config.BOARD_WIDTH/2-text.get_width()/2
            rect = pygame.Rect(text_x-50, text_y-50,
                            text.get_width()+100, text.get_height()+100)
            rect_col = (192, 192, 192)
            if i == self._user_selection:
                rect_col = (config.OVERLAY_YELLOW[0],config.OVERLAY_YELLOW[1],config.OVERLAY_YELLOW[2])
            info = {'text':text,'text_xy':(text_x,text_y),'rect_col':rect_col,'rect':rect}
            self.save_slot_information[i] = info
            text_y += 200
    
    def draw_screen(self):
        self._display.fill(config.BOARD_COLOR)
        for i in range(3):
            pygame.draw.rect(self._display,
                            self.save_slot_information[i]['rect_col'],
                            self.save_slot_information[i]['rect'],
                            border_radius=3)
            self._display.blit(self.save_slot_information[i]['text'], self.save_slot_information[i]['text_xy'])
        pygame.display.update()

    def get_user_input(self):
        user_input = ''
        self._update_save_slot_rects(user_input)
        self.draw_screen()
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
                        player_data_repository.create_player_data(user_input,self._user_selection)
                        self._existing_saves[self._user_selection] = user_input
                        return True
                    else:
                        user_input += event.unicode
                    self._update_save_slot_rects(user_input)
                    self.draw_screen()

    def main_loop(self):
        while True:
            for event in self._event_queue.get():
                self._user_selection = None
                for i, info in enumerate(self.save_slot_information):
                    if info['rect'].collidepoint(pygame.mouse.get_pos()):
                        self._user_selection = i
                        break
                self._update_save_slot_rects()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self._user_selection in self._existing_saves:
                        return player_data_repository.find_player_data(
                            self._existing_saves[self._user_selection])
                    if not self.get_user_input():
                        event.type = pygame.QUIT

                if event.type == pygame.QUIT:
                    return None
                self.draw_screen()
