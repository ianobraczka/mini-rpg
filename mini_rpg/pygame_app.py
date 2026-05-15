"""Optional pygame window: same rules as the terminal game (no second engine)."""

from __future__ import annotations

from typing import Final

# Pygame is optional so ``pytest`` and headless CI can run without it.
try:
    import pygame
except ImportError as exc:  # pragma: no cover - exercised when pygame missing
    raise SystemExit(
        "Pygame is not installed. Install with:\n"
        "  python3 -m pip install -r requirements-game.txt\n"
        "Then run: python3 -m mini_rpg.pygame_app\n"
    ) from exc

from mini_rpg.game import Game
from mini_rpg.utils import GRID_SIZE

CELL: Final[int] = 72
MARGIN: Final[int] = 24
HUD_HEIGHT: Final[int] = 100

KEY_TO_CMD: dict[int, str] = {
    pygame.K_w: "w",
    pygame.K_a: "a",
    pygame.K_s: "s",
    pygame.K_d: "d",
    pygame.K_i: "i",
    pygame.K_j: "j",
    pygame.K_k: "k",
    pygame.K_l: "l",
}


def _draw_grid(surface: pygame.Surface, font: pygame.font.Font, game: Game) -> None:
    rows = game.build_grid_rows()
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            ch = rows[y][x]
            rect = pygame.Rect(MARGIN + x * CELL, MARGIN + y * CELL, CELL, CELL)
            pygame.draw.rect(surface, (35, 40, 55), rect, border_radius=6)
            pygame.draw.rect(surface, (80, 90, 120), rect, 2, border_radius=6)
            label = font.render(ch, True, (240, 245, 255))
            surface.blit(label, label.get_rect(center=rect.center))


def _draw_hud(surface: pygame.Surface, font: pygame.font.Font, game: Game, msg: str) -> None:
    top = MARGIN * 2 + GRID_SIZE * CELL
    hp_t = f"HP: {game.player.hp}  Mana: {game.player.mana}"
    en_hp = f"Enemy HP: {game.enemies[0].hp}" if game.enemies else "Enemy: (none)"
    for i, line in enumerate((hp_t, en_hp, msg)):
        surf = font.render(line, True, (220, 225, 240))
        surface.blit(surf, (MARGIN, top + i * 28))


def main() -> None:
    """Run the RPG in a small pygame window (WASD move, IJKL attack, C = coin)."""
    pygame.init()
    pygame.display.set_caption("Mini RPG (pygame)")
    width = MARGIN * 2 + GRID_SIZE * CELL
    height = MARGIN * 2 + GRID_SIZE * CELL + HUD_HEIGHT
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("dejavusansmono", 36)

    game = Game()
    hud_msg = "Player turn — WASD move, IJKL attack (uses mana)."
    # When True, run enemy phase once on the next frame (after player spent all mana).
    run_enemy_phase_next_frame = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                elif game.game_over:
                    if event.key == pygame.K_c:
                        game.try_continue_after_gameover("coin")
                        hud_msg = "Continued! Player turn." if not game.game_over else hud_msg
                elif game.player.mana > 0:
                    cmd = KEY_TO_CMD.get(event.key)
                    if cmd:
                        game.apply_player_command(cmd)
                        hud_msg = f"Last command: {cmd!r}"
                        if game.player.mana <= 0:
                            run_enemy_phase_next_frame = True

        if run_enemy_phase_next_frame and not game.game_over:
            game.execute_enemy_phase()
            game.end_turn(interactive=False)
            run_enemy_phase_next_frame = False
            hud_msg = "Player turn — WASD / IJKL."
            if game.game_over:
                hud_msg = "Game over — press C for coin (continue) or Q to quit."

        screen.fill((18, 20, 28))
        _draw_grid(screen, font, game)
        _draw_hud(screen, font, game, hud_msg)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
