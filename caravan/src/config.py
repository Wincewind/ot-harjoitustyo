import os
import pygame
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    pass

_db_filename = os.getenv("DATABASE_FILENAME") or 'player_data.sqlite'
PATH_TO_PLAYER_DATA = os.path.join(dirname, "..", "data", _db_filename)

pygame.init()
CARD_WIDTH = 100
CARD_HEIGHT = 130
OVERLAY_GREEN = (50, 168, 82, 128)
OVERLAY_RED = (196, 65, 93, 128)
OVERLAY_YELLOW = (255, 226, 99, 128)

BOARD_WIDTH = int(os.getenv("BOARD_WIDTH")) or 1600
BOARD_HEIGHT = int(os.getenv("BOARD_HEIGHT")) or 1000
BOARD_COLOR = (53, 101, 77)
CARAVAN_BASE_COLOR = (202, 154, 178)

PLAYER_AREA_RECT = pygame.Rect(
    0, BOARD_HEIGHT - CARD_HEIGHT - 20, BOARD_WIDTH, CARD_HEIGHT+20)
OPPONENT_AREA_RECT = pygame.Rect(0, 0, BOARD_WIDTH, CARD_HEIGHT+20)

x = BOARD_WIDTH*0.4 - CARD_WIDTH
y = CARD_HEIGHT+20
w = (CARD_WIDTH + 100)*3
h = BOARD_HEIGHT - CARD_HEIGHT*2-40
CARAVAN_AREA_RECT = pygame.Rect(x, y, w, h)

PLAYER_CARAVAN_BASE_RECTS = [0, 0, 0]
x = BOARD_WIDTH*0.4 - CARD_WIDTH
y = BOARD_HEIGHT/2 + CARD_HEIGHT/2
w = CARD_WIDTH + 10
h = CARD_HEIGHT + 10
for i in range(3):
    PLAYER_CARAVAN_BASE_RECTS[i] = pygame.Rect(x, y, w, h)
    x += CARD_WIDTH + 100

OPPONENT_CARAVAN_BASE_RECTS = [0, 0, 0]
x = BOARD_WIDTH*0.4 - CARD_WIDTH
y = BOARD_HEIGHT/2 - CARD_HEIGHT
for i in range(3):
    OPPONENT_CARAVAN_BASE_RECTS[i] = pygame.Rect(x, y, w, h)
    x += CARD_WIDTH + 100


FONT = pygame.font.SysFont("Copperplate Gothic", 24)
MED_FONT = pygame.font.SysFont("Copperplate Gothic", 48)
BIG_FONT = pygame.font.SysFont("Copperplate Gothic", 64)


AVAILABLE_CARDSETS = ['sylly', 'minime453']

NPC_OPPONENT = os.getenv("NPC_OPPONENT").lower() == 'true' or False
