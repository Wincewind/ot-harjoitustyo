import copy
from entities.player import Player
from entities.caravan import Caravan
import actions
import rules


class Npc():
    """Class that performs actions for a computer opponent in the Caravan card game.

    Attributes:
        player: Player object of the computer controlled player.
        opponent: Player object of the opposing player.
    """
    def __init__(self, player: Player, opponent: Player) -> None:
        self._player = player
        self._opponent = opponent

    def _remove_overpriced_caravans(self):
        """Check if the _player object has caravans that are 
        over the max limit and discard one of them.

        Returns:
            bool: True if a caravan was sold, else False.
        """
        try:
            idx = next(i for i, caravan in enumerate(self._player.caravans) if caravan.value >
                       rules.CARAVAN_MAX)
            actions.discard_caravan(idx, self._player)
            return True
        except StopIteration:
            return False

    def _try_placing_card_in_caravan(self, crd_idx: int, crvn: Caravan,
                                     crvn_idx: int, player_copy: Player, opponent_copy: Player):
        """Try placing a selected card into a caravan.

        Args:
            crd_idx (int): Index of card in hand.
            crvn (Caravan): Caravan that the card is being placed in.
            crvn_idx (int): Index of the caravan.
            player_copy (Player): Copy of the _player attribute to test placement of a card and 
            its effect to the caravan value.
            opponent_copy (Player): Copy of the _opponent attribute to test placement of a card and 
            its effect to the caravan value.

        Returns:
            tuple(bool,int): True and the index of
            placement in caravan if playing a card was successful, False and 0 otherwise.
        """
        for i in range(len(crvn.cards)+1):
            crvn = player_copy.caravans[crvn_idx]
            crd = player_copy.hand[crd_idx]
            caravan_val = crvn.value
            move = (crvn, i, crd)
            action_success = actions.play_card(
                player_copy, opponent_copy, move)
            if action_success:
                if crvn.value >= caravan_val and crvn.value <= rules.CARAVAN_MAX:
                    return (True, i)
                player_copy = copy.copy(self._player)
                opponent_copy = copy.copy(self._opponent)
        return (False, 0)

    def _try_to_play_a_card(self):
        """Try playing cards from hand. 

        Returns:
            bool: True if a card was played successfully, else False.
        """
        player_copy = copy.copy(self._player)
        opponent_copy = copy.copy(self._opponent)
        for crd_idx, crd in enumerate(player_copy.hand):
            if crd.value not in [0, 11]:
                for crvn_idx in range(3):
                    if rules.check_if_caravan_sold(self._player.caravans[crvn_idx].value,
                                                   self._opponent.caravans[crvn_idx].value):
                        continue

                    crvn = player_copy.caravans[crvn_idx]
                    placement_desirable, i = self._try_placing_card_in_caravan(
                        crd_idx, crvn, crvn_idx, player_copy, opponent_copy)
                    if placement_desirable:
                        move = (
                            self._player.caravans[crvn_idx], i, self._player.hand[crd_idx])
                        return actions.play_card(self._player, self._opponent, move)
        return False

    def perform_action(self):
        """Perform one of 3 actions, discard a over 
         max limit caravan, try playing a card or discard one of the cards in hand. 
        """
        if self._remove_overpriced_caravans():
            return
        if self._try_to_play_a_card():
            return
        actions.discard_card(0,self._player)
        return
