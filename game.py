"""Rules for the Lantern Maze prototype."""

from enum import Enum

Position = tuple[int, int]

# '#' is a wall, '.' is a dot, and 'P' is the player's starting cell.
MAZE = (
    "###############",
    "#P............#",
    "#.##.###.###..#",
    "#....#... ....#",
    "#.##...##.###.#",
    "#....#....#.#.#",
    "###..#.#..#.#.#",
    "#....#.#......#",
    "#.##...###.##.#",
    "#.............#",
    "###############",
)

POINTS_PER_DOT = 10
GHOST_STEP_INTERVAL = 2
GHOST_PATROL = (
    (9, 3), (10, 3), (11, 3), (12, 3),
    (13, 3), (13, 4), (13, 5), (13, 6),
    (13, 7), (12, 7), (11, 7), (10, 7),
    (9, 7), (9, 6), (9, 5), (9, 4),
)


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


class State(Enum):
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


class Game:
    def __init__(self) -> None:
        self.walls: set[Position] = set()
        self.dots: set[Position] = set()
        for y, row in enumerate(MAZE):
            for x, cell in enumerate(row):
                if cell == "#":
                    self.walls.add((x, y))
                elif cell == ".":
                    self.dots.add((x, y))
                elif cell == "P":
                    self.player = (x, y)

        self.ghost = GHOST_PATROL[0]
        self.total_dots = len(self.dots)
        self.state = State.PLAYING
        self._ticks = 0

    @property
    def score(self) -> int:
        return (self.total_dots - len(self.dots)) * POINTS_PER_DOT

    def _destination(self, direction: Direction) -> Position:
        x, y = self.player
        dx, dy = direction.value
        return x + dx, y + dy

    def can_move(self, direction: Direction) -> bool:
        return self._destination(direction) not in self.walls

    def step(self, direction: Direction | None) -> None:
        """Advance one tick. A blocked move or None leaves the player in place."""
        if self.state is not State.PLAYING:
            return

        if direction is not None:
            destination = self._destination(direction)
            if destination not in self.walls:
                self.player = destination

        # Check the ghost's current cell before either character can pass through it.
        if self.player == self.ghost:
            self.state = State.LOST
            return

        self._ticks += 1
        patrol_index = (self._ticks // GHOST_STEP_INTERVAL) % len(GHOST_PATROL)
        self.ghost = GHOST_PATROL[patrol_index]
        if self.player == self.ghost:
            self.state = State.LOST
            return

        self.dots.discard(self.player)
        if not self.dots:
            self.state = State.WON
