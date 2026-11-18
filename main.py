"""Pygame window and keyboard controls for Lantern Maze."""

import pygame

from game import Direction, Game, MAZE, Position, State

TILE = 36
MARGIN = 24
BOARD = pygame.Rect(MARGIN, 82, len(MAZE[0]) * TILE, len(MAZE) * TILE)
WINDOW_SIZE = (BOARD.right + MARGIN, BOARD.bottom + 56)
STEP_INTERVAL_MS = 160

BACKGROUND = "#101920"
FLOOR = "#15232C"
WALL = "#284752"
WALL_EDGE = "#3A6069"
TEXT = "#EDF6F3"
MUTED = "#B1C6CA"
DOT = "#EBD392"
PLAYER = "#8CE2C2"
GHOST = "#F8907A"

ARROW_KEYS = {
    pygame.K_UP: Direction.UP,
    pygame.K_RIGHT: Direction.RIGHT,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
}


def cell_center(position: Position) -> Position:
    x, y = position
    return BOARD.x + x * TILE + TILE // 2, BOARD.y + y * TILE + TILE // 2


def draw_game(
    screen: pygame.Surface,
    title_font: pygame.font.Font,
    body_font: pygame.font.Font,
    game: Game,
    started: bool,
) -> None:
    screen.fill(BACKGROUND)
    screen.blit(title_font.render("Lantern Maze", True, TEXT), (MARGIN, 18))
    objective = body_font.render("Collect the dots. Avoid the wisp.", True, MUTED)
    screen.blit(objective, (MARGIN, 52))

    score = body_font.render(f"Score {game.score}", True, TEXT)
    dots = body_font.render(f"Dots left {len(game.dots)}", True, MUTED)
    screen.blit(score, score.get_rect(topright=(BOARD.right, 24)))
    screen.blit(dots, dots.get_rect(topright=(BOARD.right, 52)))

    pygame.draw.rect(screen, FLOOR, BOARD, border_radius=8)
    for x, y in game.walls:
        wall = pygame.Rect(BOARD.x + x * TILE + 1, BOARD.y + y * TILE + 1, TILE - 2, TILE - 2)
        pygame.draw.rect(screen, WALL, wall, border_radius=5)
        pygame.draw.rect(screen, WALL_EDGE, wall, width=1, border_radius=5)

    for dot in game.dots:
        pygame.draw.circle(screen, DOT, cell_center(dot), 3)

    x, y = cell_center(game.player)
    pygame.draw.polygon(screen, PLAYER, ((x, y - 13), (x + 11, y), (x, y + 13), (x - 11, y)))
    pygame.draw.circle(screen, FLOOR, (x, y), 5)
    pygame.draw.circle(screen, TEXT, (x, y), 2)

    x, y = cell_center(game.ghost)
    pygame.draw.circle(screen, GHOST, (x, y - 2), 9)
    pygame.draw.polygon(screen, GHOST, ((x - 8, y + 1), (x + 8, y + 1), (x - 2, y + 12)))
    pygame.draw.line(screen, FLOOR, (x - 4, y - 2), (x + 4, y - 2), 2)

    footer_y = BOARD.bottom + 19
    if game.state is State.PLAYING:
        control = "Arrow keys to steer" if started else "Press an arrow key to start"
        screen.blit(body_font.render(control, True, TEXT), (MARGIN, footer_y))
        shortcuts = body_font.render("R  Restart     Esc  Quit", True, MUTED)
    else:
        shortcuts = body_font.render("Esc  Quit", True, MUTED)
        shade = pygame.Surface(BOARD.size, pygame.SRCALPHA)
        shade.fill((8, 15, 21, 180))
        screen.blit(shade, BOARD.topleft)

        card = pygame.Rect(0, 0, 300, 106)
        card.center = BOARD.center
        pygame.draw.rect(screen, BACKGROUND, card, border_radius=12)
        pygame.draw.rect(screen, WALL_EDGE, card, width=1, border_radius=12)
        result = "Maze cleared" if game.state is State.WON else "Caught by the wisp"
        heading = title_font.render(result, True, TEXT)
        restart = body_font.render("Press R to play again", True, MUTED)
        screen.blit(heading, heading.get_rect(center=(card.centerx, card.y + 37)))
        screen.blit(restart, restart.get_rect(center=(card.centerx, card.y + 74)))

    screen.blit(shortcuts, shortcuts.get_rect(topright=(BOARD.right, footer_y)))
    pygame.display.flip()


def main() -> None:
    pygame.display.init()
    pygame.font.init()
    try:
        screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Lantern Maze")
        title_font = pygame.font.Font(None, 38)
        body_font = pygame.font.Font(None, 23)
        step_event = pygame.event.custom_type()
        pygame.time.set_timer(step_event, STEP_INTERVAL_MS)

        game = Game()
        direction = None
        pending = None
        draw_game(screen, title_font, body_font, game, started=False)

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_r:
                    game = Game()
                    direction = None
                    pending = None
                elif event.key in ARROW_KEYS and game.state is State.PLAYING:
                    pending = ARROW_KEYS[event.key]
            elif event.type == step_event and game.state is State.PLAYING:
                if pending is not None and game.can_move(pending):
                    direction = pending
                    pending = None
                if direction is not None:
                    game.step(direction)

            draw_game(screen, title_font, body_font, game, started=direction is not None)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
