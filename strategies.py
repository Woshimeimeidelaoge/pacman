"""Baseline policies for Lantern Maze."""

from collections import deque
from random import Random

from game import Direction, Game, Position


def random_policy(game: Game, rng: Random) -> Direction | None:
    """Choose uniformly among the directions with no wall."""
    moves = [direction for direction in Direction if game.can_move(direction)]
    return rng.choice(moves) if moves else None


def heuristic_policy(game: Game, rng: Random) -> Direction | None:
    """Take the first step toward a nearest dot, avoiding the ghost's cells."""
    ghost_cells = {game.ghost, game.next_ghost_position}
    visited = game.walls | ghost_cells | {game.player}

    # Shuffle the exploration order to break ties between equally short routes.
    directions = list(Direction)
    rng.shuffle(directions)
    frontier: deque[tuple[Position, Direction | None]] = deque([(game.player, None)])

    while frontier:
        position, first_move = frontier.popleft()
        if position in game.dots:
            return first_move

        for direction in directions:
            neighbor = direction.move_from(position)
            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append((neighbor, first_move or direction))

    # Wait for a blocked route to open, unless the ghost is about to arrive here.
    if game.player == game.next_ghost_position:
        for direction in directions:
            if game.can_move(direction) and direction.move_from(game.player) not in ghost_cells:
                return direction
    return None
