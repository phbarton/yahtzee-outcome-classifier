from src.score import Score
from src.score_category import ScoreCategory

class ScoreCard:
    """
    Represents a score card for a game, tracking scores in various categories.
    """
    def __init__(self) -> None:
        """
        Initializes an empty ScoreCard.
        """
        self.scores: dict[ScoreCategory, Score | None] = {c: None for c in ScoreCategory}
        self.upper_section_bonus_awarded: bool = False
        self.yahtzee_bonus_count: int = 0
        
    def available_categories(self) -> list[ScoreCategory]:
        """
        Returns a list of categories that have not yet been scored.
        :return: A list of available ScoreCategory enums.
        """
        return [category for category, score in self.scores.items() if score is None]

    def assign_score(self, score: Score) -> None:
        """
        Assigns a score to the appropriate category on the score card.
        :param score: The Score object to assign.
        :raises ValueError: If the category has already been scored.
        """
        if self.scores[score.category] is not None:
            raise ValueError(f"Category {score.category} has already been scored.")

        self._assign_yahtzee_bonus(score)
        self.scores[score.category] = score

    def _assign_yahtzee_bonus(self, score: Score):
        """
        Checks if the score qualifies for a Yahtzee bonus and updates the bonus count if applicable.
        :param score: The Score object to check for Yahtzee bonus.
        """
        if ScoreCard.is_yahtzee(score.roll) and self.scores[
            ScoreCategory.YAHTZEE] is not None and score.category != ScoreCategory.YAHTZEE:
            # If Yahtzee category is already filled, award a Yahtzee bonus
            self.yahtzee_bonus_count += 1

    def get_score(self, category: ScoreCategory) -> Score | None:
        """
        Retrieves the score for a specific category.
        :param category: The scoring category to retrieve.
        :return: The Score object for the category, or None if not scored yet.
        """
        return self.scores.get(category)

    @property
    def total_score(self) -> int:
        """
        Calculates the total score, including any bonuses.
        :return: The total score as an integer.
        """
        total = sum(score.points for score in self.scores.values() if score is not None)
        
        self._check_upper_section_bonus()
        
        if self.upper_section_bonus_awarded:
            total += 35
        
        total += self.yahtzee_bonus_count * 100
        
        return total

    def __repr__(self) -> str:
        """
        Returns a string representation of the ScoreCard instance.
        :return: A string representing the ScoreCard instance.
        """
        return f"ScoreCard(scores={self.scores})"
    
    def _check_upper_section_bonus(self) -> None:
        """
        Checks if the upper section bonus has been achieved and updates the status.
        """
        if self.upper_section_bonus_awarded:
            return
        
        upper_section_total = sum(
            score.points for category, score in self.scores.items()
            if category in [
                ScoreCategory.ACES,
                ScoreCategory.TWOS,
                ScoreCategory.THREES,
                ScoreCategory.FOURS,
                ScoreCategory.FIVES,
                ScoreCategory.SIXES
            ] and score is not None
        )
        
        if upper_section_total >= 63:
            self.upper_section_bonus_awarded = True
            
    @staticmethod
    def is_yahtzee(roll: list[int]) -> bool:
        """
        Checks if the given roll is a Yahtzee (all dice the same).
        :param roll: A list of integers representing the dice roll.
        :return: True if the roll is a Yahtzee, False otherwise.
        """
        return len(set(roll)) == 1 and len(roll) == 5