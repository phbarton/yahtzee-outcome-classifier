from typing import Any

from src.score_category import ScoreCategory


class Score:
    """
    Represents a score in a specific category based on a roll of dice.
    """
    def __init__(self, category: ScoreCategory, roll: list[int], points: int) -> None:
        """
        Initializes a Score instance.
        :param category: The scoring category.
        :param roll: The list of dice values.
        :param points: The points scored in this category.
        """
        self.category = category
        self.roll = roll
        self.points = points

    def __repr__(self) -> str:
        """
        Returns a string representation of the Score instance.
        :return: A string representing the Score instance.
        """
        return f"Score(category={self.category}, roll={self.roll}, points={self.points})"
    
    def to_dict(self) -> dict[str, Any]:
        """
        Converts the Score instance to a dictionary.
        :return: A dictionary representation of the Score instance.
        """
        return {
            'category': self.category.value,
            'roll': self.roll,
            'points': self.points
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Score':
        """
        Creates a Score instance from a dictionary.
        :param data: A dictionary containing the score data.
        :return: A Score instance.
        """
        category = ScoreCategory(data['category'])
        roll = data['roll']
        points = data['points']
        return cls(category, roll, points)
