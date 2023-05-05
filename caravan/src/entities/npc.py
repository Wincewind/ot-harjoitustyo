import copy
from entities.player import Player
from entities.caravan import Caravan
import actions
import rules


class Npc():
    def __init__(self, player: Player, opponent: Player) -> None:
        self._player = player
        self._opponent = opponent

    def _remove_overpriced_caravans(self):
        try:
            idx = next(i for i, caravan in enumerate(self._player.caravans) if caravan.value >
                       rules.CARAVAN_MAX)
            actions.discard_caravan(idx, self._player)
            return True
        except StopIteration:
            return False

    def _try_placing_card_in_caravan(self, crd_idx: int, crvn: Caravan,
                                     crvn_idx: int, player_copy: Player, opponent_copy: Player):
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
                #crd = player_copy.hand[crd_idx]
                opponent_copy = copy.copy(self._opponent)
        return (False, 0)

    def _try_to_play_a_card(self):
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
        if self._remove_overpriced_caravans():
            return
        if self._try_to_play_a_card():
            return
        actions.discard_card(0,self._player)
        return
