"""Combat-focused tests (list cleanup, defeat condition, spawn after wipe)."""

from __future__ import annotations

from unittest import mock

from mini_rpg.combat import player_is_defeated, remove_dead_enemies
from mini_rpg.enemy import Elf, Enemy
from mini_rpg.game import Game


def test_victory_flow_respawns_enemy_when_list_empty() -> None:
    """After the last enemy dies, a new enemy should spawn (random choice mocked)."""
    g = Game()
    g.enemies.clear()
    with mock.patch("mini_rpg.game.random.randint", return_value=1):
        g._spawn_enemies_if_empty()
    assert len(g.enemies) == 1
    assert isinstance(g.enemies[0], Elf)


def test_defeat_sets_game_over_until_coin(monkeypatch) -> None:
    g = Game()
    g.player.hp = 0
    inputs = iter(["no_coin"])
    monkeypatch.setattr("mini_rpg.game.cli.prompt_continue_after_gameover", lambda: next(inputs))
    g.check_game_over()
    assert g.game_over is True


def test_continue_with_coin_resets_game(monkeypatch) -> None:
    g = Game()
    g.player.hp = 0
    monkeypatch.setattr("mini_rpg.game.cli.prompt_continue_after_gameover", lambda: "coin")
    g.check_game_over()
    assert g.game_over is False
    assert g.player.hp == 10
    assert len(g.enemies) >= 1


def test_remove_dead_preserves_order_of_survivors() -> None:
    a = Enemy.__new__(Enemy)
    a.hp = 1
    b = Enemy.__new__(Enemy)
    b.hp = 0
    c = Enemy.__new__(Enemy)
    c.hp = 2
    lst = [a, b, c]
    remove_dead_enemies(lst)
    assert [e.hp for e in lst] == [1, 2]


def test_player_is_defeated_boundary() -> None:
    assert player_is_defeated(0)
    assert not player_is_defeated(10)
