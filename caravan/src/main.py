import pygame
import config
import gameloop
from entities.cardset import CardSet
from entities.player_data import PlayerData
from ui.eventqueue import EventQueue
from ui.renderer import Renderer
from ui.gamesprites import GameSprites
from ui.save_selection import SaveSelection
from ui.deck_creation import DeckCreation

def main():
    """Main function to run to handle the game UIs, init player data and start the gameloop.
    """
    display = pygame.display.set_mode(
        (config.BOARD_WIDTH, config.BOARD_HEIGHT))
    event_queue = EventQueue()
    save_screen = SaveSelection(display, event_queue)
    pl_data = save_screen.main_loop()
    if pl_data is not None:
        deck_creation = DeckCreation(display, event_queue, pl_data)
        player = deck_creation.main_loop()
        if player is not None:
            opponent_data = PlayerData('Opponent', 0, 0, -1, [CardSet.sets[0]])
            opponent = opponent_data.prepare_player(CardSet.sets[0])
            game_sprites = GameSprites(display, player, opponent)
            renderer = Renderer(display, game_sprites)
            game_loop = gameloop.GameLoop(
                renderer, game_sprites, event_queue, (pl_data.name,pl_data.row_number))
            game_loop.start()


if __name__ == "__main__":
    main()
