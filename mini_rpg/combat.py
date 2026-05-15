"""Combat helpers: removing dead enemies (safe list updates)."""

from __future__ import annotations

from mini_rpg.enemy import Enemy


def remove_dead_enemies(enemies: list[Enemy]) -> None:
    """Drop enemies with hp <= 0 (mutates list in place; avoids remove-while-iterating bugs)."""
    enemies[:] = [e for e in enemies if e.hp > 0]


def player_is_defeated(player_hp: int) -> bool:
    """Return True if the player has no HP left."""
    return player_hp <= 0
