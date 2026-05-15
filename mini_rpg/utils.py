"""Small helpers shared by entities and the game (no I/O here)."""

from __future__ import annotations

import random

# Grid is 5×5, indices 0–4 (matches the original game).
GRID_SIZE: int = 5
START_MANA: int = 2


def random_cell_not_on_player(player_x: int, player_y: int) -> tuple[int, int]:
    """Return a random (x, y) on the grid, retrying if it would overlap the player."""
    for _ in range(50):
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if x != player_x or y != player_y:
            return x, y
    return 0, 0
