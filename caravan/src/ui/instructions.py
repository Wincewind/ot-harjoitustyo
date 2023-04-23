import pygame
import config


def write_game_controls(display):
    font_color = (255, 255, 255)
    instructions = {"Space bar": ["Start turn /", "Select card /",
                                  "Confirm card placement in caravan: "],
                    "Arrow keys": ["Card selection /",
                                   "Switching card position in caravans: "],
                    "Esc": ["Cancel selection: "]}
    text = config.FONT.render('', True, font_color)
    instructions_x = 0
    instructions_y = -text.get_height()
    for instruction in instructions.items():
        for action in instruction[1]:
            instructions_y = instructions_y+5+text.get_height()
            text = config.FONT.render(action, True, font_color)
            display.blit(text, (instructions_x, instructions_y))
        input_x = text.get_width() + 5
        text = config.FONT.render(instruction[0], True, (255, 226, 99))
        display.blit(text, (input_x, instructions_y))
        instructions_y = instructions_y+text.get_height()/2


def game_over_message(winning_player_num: int, display):
    font_color = (0, 0, 0)
    msg = 'Player '+str(winning_player_num)+" is the winner! Congratulations!"
    text = config.BIG_FONT.render(msg, True, font_color)
    text_x = config.BOARD_WIDTH/2-text.get_width()/2
    text_y = config.BOARD_HEIGHT/2-text.get_height()

    rect = pygame.Rect(text_x-100, text_y-100,
                       text.get_width()+200, text.get_height()+200)
    pygame.draw.rect(display,
                     (192, 192, 192),
                     rect,
                     border_radius=3)
    display.blit(text, (text_x, text_y))
