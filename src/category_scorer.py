from collections import Counter
from typing import Callable

from src.score import Score
from src.score_category import ScoreCategory

CATEGORY_SCORERS: dict[str, Callable[[list[int]], Score | None]] = {
    ScoreCategory.ACES.value: lambda roll: sum_roll_by_value(roll, ScoreCategory.ACES, 1),
    ScoreCategory.TWOS.value: lambda roll: sum_roll_by_value(roll, ScoreCategory.TWOS, 2),
    ScoreCategory.THREES.value: lambda roll: sum_roll_by_value(roll, ScoreCategory.THREES, 3),
    ScoreCategory.FOURS.value: lambda roll: sum_roll_by_value(roll, ScoreCategory.FOURS, 4),
    ScoreCategory.FIVES.value: lambda roll: sum_roll_by_value(roll, ScoreCategory.FIVES, 5),
    ScoreCategory.SIXES.value: lambda roll: sum_roll_by_value(roll, ScoreCategory.SIXES, 6),
    ScoreCategory.THREE_OF_A_KIND.value: lambda roll: sum_n_of_a_kind(roll, 3),
    ScoreCategory.FOUR_OF_A_KIND.value: lambda roll: sum_n_of_a_kind(roll, 4),
    ScoreCategory.FULL_HOUSE.value: lambda roll: score_full_house(roll),
    ScoreCategory.SMALL_STRAIGHT.value: lambda roll: score_small_straight(roll),
    ScoreCategory.LARGE_STRAIGHT.value: lambda roll: score_large_straight(roll),
    ScoreCategory.YAHTZEE.value: lambda roll: score_yahtzee(roll),
    ScoreCategory.CHANCE.value: lambda roll: Score(ScoreCategory.CHANCE, roll, sum(roll)),
}

def sum_roll_by_value(roll: list[int], category: ScoreCategory, value: int) -> Score | None:
    """Calculate the score for a roll based on the specified die value.

    Args:
        roll (list[int]): The list of dice values in the roll.
        category (ScoreCategory): The scoring category.
        value (int): The die value to sum (1-6).

    Returns:
        Score | None: The calculated score or None if no dice match the value.
    """
    if value < 1 or value > 6:
        raise ValueError("Value must be between 1 and 6.")
    score = sum(die for die in roll if die == value)
    return Score(category, roll, score) if score > 0 else None

def sum_n_of_a_kind(roll: list[int], n: int) -> Score | None:
    """Calculate the score for n-of-a-kind in a roll.

    Args:
        roll (list[int]): The list of dice values in the roll.
        n (int): The number of identical dice required (e.g., 3 for three-of-a-kind).

    Returns:
        Score | None: The calculated score or None if the condition is not met.
    """
    if n < 1 or n > 5:
        raise ValueError("n must be between 1 and 5.")
    
    counts = Counter(roll)
    
    if any(count >= n for count in counts.values()):
        return Score(ScoreCategory.THREE_OF_A_KIND if n == 3 else ScoreCategory.FOUR_OF_A_KIND, roll, sum(roll))
    
    return None

def score_full_house(roll: list[int]) -> Score | None:
    """Calculate the score for a full house in a roll.

    Args:
        roll (list[int]): The list of dice values in the roll.

    Returns:
        Score | None: The calculated score or None if the condition is not met.
    """
    counts = Counter(roll)
    
    if sorted(counts.values()) == [2, 3]:
        return Score(ScoreCategory.FULL_HOUSE, roll, 25)
    
    return None

def score_small_straight(roll: list[int]) -> Score | None:
    """Calculate the score for a small straight in a roll.

    Args:
        roll (list[int]): The list of dice values in the roll.

    Returns:
        Score | None: The calculated score or None if the condition is not met.
    """
    unique_roll = set(roll)
    small_straights = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
    
    if any(straight.issubset(unique_roll) for straight in small_straights):
        return Score(ScoreCategory.SMALL_STRAIGHT, roll, 30)
    
    return None

def score_large_straight(roll: list[int]) -> Score | None:
    """Calculate the score for a large straight in a roll.

    Args:
        roll (list[int]): The list of dice values in the roll.

    Returns:
        Score | None: The calculated score or None if the condition is not met.
    """
    unique_roll = set(roll)
    large_straights = [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]
    
    if any(straight == unique_roll for straight in large_straights):
        return Score(ScoreCategory.LARGE_STRAIGHT, roll, 40)
    
    return None

def score_yahtzee(roll: list[int]) -> Score | None:
    """Calculate the score for a Yahtzee in a roll.

    Args:
        roll (list[int]): The list of dice values in the roll.

    Returns:
        Score | None: The calculated score or None if the condition is not met.
    """
    if len(set(roll)) == 1:
        return Score(ScoreCategory.YAHTZEE, roll, 50)
    
    return None