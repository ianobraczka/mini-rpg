"""Enemy entities and simple chase AI."""

from __future__ import annotations

import random

from mini_rpg.utils import random_cell_not_on_player


class Enemy:
    """Base enemy: chases the player and attacks when adjacent."""

    symbol: str = "!"
    hp: int = 4

    def __init__(self, player_x: int, player_y: int) -> None:
        self.cooldown: float = 2
        self.speed: int = 1
        self.damage: int = 2
        self.symbol = "!"
        self.hp = 4
        self.position_x, self.position_y = random_cell_not_on_player(player_x, player_y)

    def play(self, player_x: int, player_y: int, player: object) -> None:
        """Take one turn: move toward the player or attack if already next to them."""
        from mini_rpg.player import Player

        assert isinstance(player, Player)

        if self.position_x > player_x:
            if self.position_x - 1 == player_x and self.position_y == player_y:
                player.hp -= self.damage
            else:
                self.position_x -= 1
        elif self.position_x < player_x:
            if self.position_x + 1 == player_x and self.position_y == player_y:
                player.hp -= self.damage
            else:
                self.position_x += 1
        else:
            if self.position_y > player_y:
                if self.position_x == player_x and self.position_y - 1 == player_y:
                    player.hp -= self.damage
                else:
                    self.position_y -= 1
            elif self.position_y < player_y:
                if self.position_x == player_x and self.position_y + 1 == player_y:
                    player.hp -= self.damage
                else:
                    self.position_y += 1


class Elf(Enemy):
    """Weaker enemy with less HP."""

    def __init__(self, player_x: int, player_y: int) -> None:
        super().__init__(player_x, player_y)
        self.symbol = "1"
        self.hp = 2
        self.damage = 1


class Orc(Enemy):
    """Tougher enemy with more HP."""

    def __init__(self, player_x: int, player_y: int) -> None:
        super().__init__(player_x, player_y)
        self.symbol = "2"
        self.hp = 5
        self.damage = 1
