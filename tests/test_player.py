"""Tests for Player creation and basic combat interactions."""

from __future__ import annotations

from mini_rpg.combat import player_is_defeated, remove_dead_enemies
from mini_rpg.enemy import Enemy, Orc
from mini_rpg.player import Player


def test_player_creation_default_stats() -> None:
    p = Player()
    assert p.hp == 10
    assert p.mana == 2
    assert p.damage == 2
    assert (p.position_x, p.position_y) == (2, 2)


def test_enemy_creation_has_hp_and_symbol() -> None:
    e = Enemy(2, 2)
    assert e.hp == 4
    assert e.symbol == "!"
    assert 0 <= e.position_x <= 4
    assert 0 <= e.position_y <= 4


def test_damage_adjacent_attack_reduces_enemy_hp() -> None:
    """Attack key 'i' hits the enemy tile where enemy.position_y + 1 == player.position_y."""
    p = Player()
    p.position_x, p.position_y = 2, 2
    p.mana = 2
    enemy = Enemy.__new__(Enemy)  # bypass random spawn
    enemy.hp = 5
    enemy.position_x = 2
    enemy.position_y = 1
    enemy.damage = 1
    enemy.symbol = "x"
    enemies = [enemy]

    assert p.play("i", enemies) is True
    assert enemy.hp == 3  # 5 - player.damage (2)


def test_remove_dead_enemies_filters_list() -> None:
    e1 = Enemy.__new__(Enemy)
    e1.hp = 0
    e1.position_x = e1.position_y = 0
    e2 = Enemy.__new__(Enemy)
    e2.hp = 3
    e2.position_x = e2.position_y = 1
    lst = [e1, e2]
    remove_dead_enemies(lst)
    assert len(lst) == 1
    assert lst[0].hp == 3


def test_player_defeated_when_hp_zero() -> None:
    assert player_is_defeated(0) is True
    assert player_is_defeated(-1) is True
    assert player_is_defeated(1) is False


def test_enemy_attack_reduces_player_hp() -> None:
    """Enemy adjacent to the left of the player should damage on its turn."""
    p = Player()
    p.position_x, p.position_y = 2, 2
    p.hp = 10
    enemy = Orc(2, 2)
    enemy.position_x = 1
    enemy.position_y = 2
    enemy.play(2, 2, p)
    assert p.hp < 10
