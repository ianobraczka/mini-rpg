# Mini RPG

Small **terminal-based** RPG used to teach **clean Python layout**, **objects**, and **separation of concerns** without building a heavy “engine”.

## Purpose

- Show how to split **entities**, **combat rules**, **game flow**, and **terminal I/O** into different modules.
- Stay small enough for students or beginners to read in one sitting.

## How to run the game

From the repository root:

```bash
python3 -m mini_rpg
```

Controls (same as the original prototype):

- **Move** (1 mana): `w` `a` `s` `d`
- **Attack** (2 mana): `i` `j` `k` `l` (directional melee next to the player)
- After you run out of mana, **enemies** take their turns.
- On **game over**, type `coin` at the prompt to reset (original behaviour).

## How to run tests

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest
```

## Architecture (short)

| Module | Role |
|--------|------|
| `mini_rpg/player.py` | `Player` stats, movement, attacks |
| `mini_rpg/enemy.py` | `Enemy`, `Elf`, `Orc` and simple chase AI |
| `mini_rpg/combat.py` | Safe removal of dead enemies, defeat check |
| `mini_rpg/items.py` | `Item` dataclass placeholder for future exercises |
| `mini_rpg/cli.py` | Printing the grid and reading input (no rules) |
| `mini_rpg/game.py` | `Game` class: turn flow, spawning, game-over handling |
| `mini_rpg/utils.py` | Grid size constants and small helpers |
| `mini_rpg/__main__.py` | `python -m mini_rpg` entry point |

**Intentionally simple:** no ECS, no plugins, no asset pipeline—just readable modules you can extend (e.g. real items, more enemy types, a proper grid library).

## Requirements

- Python **3.10+** (uses modern type hints like `list[str]`).
