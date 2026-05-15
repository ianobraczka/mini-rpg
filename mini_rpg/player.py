"""Player entity: stats, movement, and melee attacks."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mini_rpg.utils import GRID_SIZE, START_MANA

if TYPE_CHECKING:
    from mini_rpg.enemy import Enemy


class Player:
    """The human-controlled character on a small toroidal grid."""

    def __init__(self) -> None:
        self.hp: int = 10
        self.mana: int = START_MANA
        self.cooldown: float = 0.5
        self.speed: int = 2
        self.damage: int = 2
        self.position_x: int = 2
        self.position_y: int = 2

    def play(self, jogada: str, enemy_list: list[Enemy]) -> bool:
        """Spend mana for a move or attack. Returns True if the action was accepted."""
        if jogada in ("w", "s", "d", "a"):
            if self.mana > 0:
                self.mana -= 1
                self.walk(jogada, enemy_list)
                return True
        elif jogada in ("i", "k", "j", "l"):
            if self.mana >= 2:
                self.mana -= 2
                self.hit(jogada, enemy_list)
                return True
        return False

    def walk(self, jogada: str, enemy_list: list[Enemy]) -> None:
        """Move one step (toroidal grid). Blocked if an enemy occupies the target tile."""
        max_i = GRID_SIZE - 1

        if jogada == "w":
            for enemy in enemy_list:
                if self.position_x == enemy.position_x and self.position_y == enemy.position_y + 1:
                    return
            self.position_y = max_i if self.position_y == 0 else self.position_y - 1

        elif jogada == "s":
            for enemy in enemy_list:
                if self.position_x == enemy.position_x and self.position_y == enemy.position_y - 1:
                    return
            self.position_y = 0 if self.position_y == max_i else self.position_y + 1

        elif jogada == "d":
            for enemy in enemy_list:
                if self.position_x == enemy.position_x - 1 and self.position_y == enemy.position_y:
                    return
            self.position_x = 0 if self.position_x == max_i else self.position_x + 1

        elif jogada == "a":
            for enemy in enemy_list:
                if self.position_x == enemy.position_x + 1 and self.position_y == enemy.position_y:
                    return
            self.position_x = max_i if self.position_x == 0 else self.position_x - 1

    def hit(self, jogada: str, enemy_list: list[Enemy]) -> None:
        """Spend 2 mana to strike an adjacent enemy (original directional mapping)."""
        max_i = GRID_SIZE - 1

        if jogada == "i":
            for enemy in enemy_list:
                if self.position_x == enemy.position_x and self.position_y == enemy.position_y + 1:
                    enemy.hp -= self.damage

        elif jogada == "k":
            for enemy in enemy_list:
                if self.position_x == enemy.position_x and self.position_y == enemy.position_y - 1:
                    enemy.hp -= self.damage

        elif jogada == "l":
            for enemy in enemy_list:
                if self.position_x == enemy.position_x - 1 and self.position_y == enemy.position_y:
                    enemy.hp -= self.damage

        elif jogada == "j":
            for enemy in enemy_list:
                if self.position_x == enemy.position_x + 1 and self.position_y == enemy.position_y:
                    enemy.hp -= self.damage

            # Preserved from original player.py (likely unintended but kept for identical behaviour).
            if self.position_y == max_i:
                self.position_y = 0
            else:
                self.position_y += 1

            if self.position_y == 0:
                self.position_y = max_i
            else:
                self.position_y -= 1
