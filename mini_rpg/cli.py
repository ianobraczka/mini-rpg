"""Terminal input/output for the game (no game rules here)."""

from __future__ import annotations

from typing import Sequence


def clear_screen(*, blank_lines: int = 50) -> None:
    """Cheap 'clear' using blank lines (same approach as the original game)."""
    for _ in range(blank_lines):
        print("")


def render_grid(rows: Sequence[Sequence[str]]) -> None:
    """Print each row of the ASCII grid."""
    for row in rows:
        print(list(row))


def render_status(
    *,
    player_hp: int,
    player_mana: int,
    enemy_hp_display: str,
) -> None:
    """Show HP/mana bars and optional enemy HP text."""
    print("")
    print("vida do player:", player_hp * "♥ ")
    print("mana do player:", player_mana * "✰ ")
    print("vida do inimigo:", enemy_hp_display)
    print("")


def prompt_move(message: str = "diga a sua jogada\n") -> str:
    """Read one line of input from the player."""
    return input(message)


def prompt_continue_after_gameover() -> str:
    """Original 'insert coin' continue prompt."""
    return input("gameover insert a coin to continue . . .\n")
