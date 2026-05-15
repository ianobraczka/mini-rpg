# Mini RPG

Small **grid-based** RPG used to teach **clean Python layout**, **objects**, and **separation of concerns** without building a heavy “engine”.

> **Note:** This repository’s git history has always been **terminal-based** (`print` / `input`). There was no earlier pygame version in this repo. The **pygame window** is an **optional front-end** that reuses the same `Game` logic.

## Purpose

- Show how to split **entities**, **combat rules**, **game flow**, and **I/O** (terminal vs. window) into different modules.
- Stay small enough for students or beginners to read in one sitting.

## How to run the game

### Terminal (original style)

```bash
python3 -m mini_rpg
```

### Pygame window (optional)

```bash
python3 -m pip install -r requirements-game.txt
python3 -m mini_rpg.pygame_app
```

Controls (both modes):

- **Move** (1 mana): `w` `a` `s` `d` — in pygame use **W A S D**
- **Attack** (2 mana): `i` `j` `k` `l` — in pygame use **I J K L**
- After mana runs out, **enemies** take their turns (pygame runs this automatically after your last move).
- **Game over:** terminal asks you to type `coin`; pygame asks you to press **C** for coin (same reset).

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
| `mini_rpg/cli.py` | Terminal grid + blocking input |
| `mini_rpg/game.py` | `Game` class: turn flow, spawning, game-over handling |
| `mini_rpg/utils.py` | Grid size constants and small helpers |
| `mini_rpg/pygame_app.py` | Optional pygame UI (same rules, no duplicate combat code) |
| `mini_rpg/__main__.py` | `python -m mini_rpg` → terminal |

**Intentionally simple:** no ECS, no plugins, no asset pipeline—just readable modules you can extend.

## Requirements

- Python **3.10+** (uses modern type hints like `list[str]`).
- **Pygame** only if you use the window (see `requirements-game.txt`).
