import numpy as np

class DiceRoller:
    """
    A class to simulate rolling and rerolling dice.
    """
    def __init__(self, num_dice: int = 5, die_size: int = 6, seed: int =None) -> None:
        """
        Initialize the DiceRoller with a specified number of dice and an optional random seed.
        :param num_dice: Number of dice used in a roll.
        :param seed: Optional seed for the random number generator.
        """
        self.num_dice = num_dice
        self.die_size = die_size
        self.rng = np.random.default_rng(seed)

    def roll(self) -> list[int]:
        """
        Roll the specified number of dice.
        :return: A list of integers representing the result of each die rolled.
        """
        return sorted(self._roll_dice(self.num_dice))
    
    def reroll(self, dice: list[int], indices: list[int]) -> list[int]:
        """
        Reroll specific dice based on their indices.
        :param dice: The current list of dice values.
        :param indices: List of indices of dice to reroll.
        :return: A new list of integers representing the updated dice values after rerolling.
        """
        new_dice = dice.copy()
        
        # Reroll the specified dice
        for index in indices:
            # Ensure the index is valid
            if 0 <= index < self.num_dice:
                roll = self._roll_dice()[0]
                new_dice[index] = roll
                
        # Return the new sorted list of dice
        return sorted(new_dice)
        
    def _roll_dice(self, num: int = 1) -> list[int]:
        """
        Roll a specified number of dice.
        :param num: Number of dice to roll.
        :return: A list of integers representing the result of each die rolled.
        """
        return self.rng.integers(1, self.die_size + 1, size=num).tolist()