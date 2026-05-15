"""Game loop and world state: ties together entities, combat cleanup, and CLI."""

from __future__ import annotations

import random

from mini_rpg import cli
from mini_rpg import combat
from mini_rpg.enemy import Elf, Enemy, Orc
from mini_rpg.player import Player
from mini_rpg.utils import GRID_SIZE


class Game:
    """Owns the player, enemy list, and high-level turn flow."""

    def __init__(self) -> None:
        self.player = Player()
        self.enemies: list[Enemy] = []
        self.game_over: bool = False
        self._spawn_initial_enemy()

    def _spawn_initial_enemy(self) -> None:
        self.enemies.append(Enemy(self.player.position_x, self.player.position_y))

    def build_grid_rows(self) -> list[list[str]]:
        """5×5 grid with player (웃) and enemy symbols."""
        rows: list[list[str]] = [["_" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        rows[self.player.position_y][self.player.position_x] = "웃"
        for enemy in self.enemies:
            rows[enemy.position_y][enemy.position_x] = enemy.symbol
        return rows

    def render(self) -> None:
        """Draw the current state to the terminal."""
        cli.clear_screen()
        cli.render_grid(self.build_grid_rows())
        enemy_hp = str(self.enemies[0].hp) + " HP" if self.enemies else "(nenhum)"
        cli.render_status(
            player_hp=self.player.hp,
            player_mana=self.player.mana,
            enemy_hp_display=enemy_hp,
        )

    def apply_player_command(self, move: str) -> bool:
        """Apply one player command (move or attack). Returns True if mana was spent."""
        ok = self.player.play(move, self.enemies)
        if ok:
            combat.remove_dead_enemies(self.enemies)
            self._spawn_enemies_if_empty()
        return ok

    def run_player_phase(self) -> None:
        """Player spends mana on moves/attacks until mana is 0 (terminal; uses blocking input)."""
        while self.player.mana > 0:
            self.render()
            move = cli.prompt_move()
            self.apply_player_command(move)

    def execute_enemy_phase(self) -> None:
        """Each living enemy takes one turn (no rendering)."""
        for enemy in list(self.enemies):
            enemy.play(self.player.position_x, self.player.position_y, self.player)

    def run_enemy_phase(self) -> None:
        """Enemy phase with terminal rendering before and after."""
        self.render()
        self.execute_enemy_phase()
        self.render()

    def _spawn_enemies_if_empty(self) -> None:
        if len(self.enemies) == 0:
            choice = random.randint(1, 2)
            if choice == 1:
                enemy: Enemy = Elf(self.player.position_x, self.player.position_y)
            else:
                enemy = Orc(self.player.position_x, self.player.position_y)
            self.enemies.append(enemy)

    def player_is_dead(self) -> bool:
        return combat.player_is_defeated(self.player.hp)

    def try_continue_after_gameover(self, coin: str) -> None:
        """If input is the magic string ``coin``, reset (same as original terminal game)."""
        if coin == "coin":
            self.game_over = False
            self.reset()

    def check_game_over(self, *, interactive: bool = True) -> None:
        """
        If the player has no HP, enter game-over state.
        When ``interactive`` is True, prompt in the terminal for ``coin`` to continue.
        """
        if not self.player_is_dead():
            return
        self.game_over = True
        if interactive:
            coin = cli.prompt_continue_after_gameover()
            self.try_continue_after_gameover(coin)

    def reset(self) -> None:
        """Restart world state (original reset behaviour)."""
        self.player = Player()
        self.enemies = []
        self._spawn_initial_enemy()

    def end_turn(self, *, interactive: bool = True) -> None:
        """After enemy phase: game-over check and refresh player mana."""
        self.check_game_over(interactive=interactive)
        self.player.mana = 2

    def run_turn(self) -> None:
        """One full round: player phase, enemy phase, refresh mana, game-over check."""
        self.run_player_phase()
        self.run_enemy_phase()
        self.end_turn(interactive=True)

    def run(self) -> None:
        """Main loop until game_over stays True (only after game over without coin)."""
        self.render()
        while not self.game_over:
            self.run_turn()


def main() -> None:
    """Entry point used by ``python -m mini_rpg``."""
    Game().run()


if __name__ == "__main__":
    main()
