from src.category_scorer import CATEGORY_SCORERS
from src.score import Score


class Scorer:
    """
    Scorer class to evaluate a roll of dice and return possible scores for each valid category.
    """
    def __init__(self, min_dice: int = 5):
        """
        Initializes the Scorer with predefined category scorers.
        """
        self._category_scorers = CATEGORY_SCORERS
        self._min_dice = min_dice

    def get_scores(self, roll: list[int]) -> list[Score]:
        """
        Evaluates the roll and returns a list of possible scores for each valid category.
        :param roll: A list of integers representing the dice roll.
        :return: A list of Score objects for each valid scoring category.
        """
        scores = []
        
        if len(roll) < self._min_dice:
            return scores
        
        for _, scorer in self._category_scorers.items():
            score = scorer(roll)
            
            if score is not None:
                scores.append(score)
                
        return scores