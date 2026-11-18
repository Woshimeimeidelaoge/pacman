"""Run and compare Lantern Maze policies without a display."""

import argparse
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from random import Random
from statistics import fmean
from time import perf_counter

from game import Direction, Game, State
from strategies import heuristic_policy, random_policy

DEFAULT_MAX_STEPS = 500
DEFAULT_SEED = 42

Policy = Callable[[Game, Random], Direction | None]
STRATEGIES: dict[str, Policy] = {"random": random_policy, "heuristic": heuristic_policy}


@dataclass(frozen=True)
class EpisodeResult:
    """Final score, turns played, and state. A playing state indicates a timeout."""

    score: int
    steps: int
    state: State


def run_episode(
    policy: Policy, *, max_steps: int = DEFAULT_MAX_STEPS, seed: int = DEFAULT_SEED
) -> EpisodeResult:
    """Run a fresh game. The policy reads the game state and returns its next move."""
    if max_steps < 1:
        raise ValueError("max_steps must be a positive integer")

    game = Game()
    rng = Random(seed)
    for steps in range(1, max_steps + 1):
        game.step(policy(game, rng))
        if game.state is not State.PLAYING:
            break

    return EpisodeResult(score=game.score, steps=steps, state=game.state)


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strategy", choices=("both", *STRATEGIES), default="both")
    parser.add_argument("--episodes", type=positive_int, default=30)
    parser.add_argument("--max-steps", type=positive_int, default=DEFAULT_MAX_STEPS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()

    names = tuple(STRATEGIES) if args.strategy == "both" else (args.strategy,)
    print(f"Episodes per strategy {args.episodes}    Max steps {args.max_steps}    Seed {args.seed}")
    print(
        f"{'Strategy':<10} {'Avg score':>9} {'Wins':>6} {'Losses':>6} {'Timeouts':>8} "
        f"{'Win rate':>9} {'Avg steps':>9} {'Total (s)':>9}"
    )

    for name in names:
        start = perf_counter()
        results = [
            run_episode(STRATEGIES[name], max_steps=args.max_steps, seed=args.seed + episode)
            for episode in range(args.episodes)
        ]
        elapsed = perf_counter() - start
        states = Counter(result.state for result in results)
        wins = states[State.WON]
        win_rate = wins / args.episodes
        mean_score = fmean(result.score for result in results)
        mean_steps = fmean(result.steps for result in results)
        print(
            f"{name:<10} {mean_score:9.1f} {wins:6d} {states[State.LOST]:6d} {states[State.PLAYING]:8d} "
            f"{win_rate:9.1%} {mean_steps:9.1f} {elapsed:9.3f}"
        )


if __name__ == "__main__":
    main()
