import json
import os

SCOREBOARD_FILE = "./Data/scoreboard.json"
MAX_SCORES = 5


def load_scores() -> list[int]:
    if not os.path.exists(SCOREBOARD_FILE):
        return []
    with open(SCOREBOARD_FILE) as f:
        return json.load(f)


def save_scores(scores: list[int]) -> None:
    with open(SCOREBOARD_FILE, "w") as f:
        json.dump(scores, f)


def add_score(score: int) -> int | None:
    scores = load_scores()
    scores.append(score)
    scores.sort(reverse=True)
    scores = scores[:MAX_SCORES]
    save_scores(scores)
    rank = scores.index(score)
    if rank < MAX_SCORES:
        return rank + 1
    return None
