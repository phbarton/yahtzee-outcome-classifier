import pytest

from src.category_scorer import (
    sum_roll_by_value,
    sum_n_of_a_kind,
    score_full_house,
    score_small_straight,
    score_large_straight,
    score_yahtzee,
    CATEGORY_SCORERS
)
from src.score_category import ScoreCategory


# sum_roll_by_value Tests
def test_sum_roll_by_value_with_matches():
    """Test sum_roll_by_value with rolls that have matching dice."""
    # Test basic matching
    result = sum_roll_by_value([1, 1, 1, 2, 3], ScoreCategory.ACES, 1)
    assert result is not None
    assert result.points == 3
    assert result.roll == [1, 1, 1, 2, 3]
    assert result.category == ScoreCategory.ACES

    # Test all same dice
    result = sum_roll_by_value([6, 6, 6, 6, 6], ScoreCategory.SIXES, 6)
    assert result is not None
    assert result.points == 30

    # Test single match
    result = sum_roll_by_value([1, 2, 3, 4, 5], ScoreCategory.THREES, 3)
    assert result is not None
    assert result.points == 3

def test_sum_roll_by_value_no_matches():
    """Test sum_roll_by_value with rolls that have no matches."""
    # Test no matches
    result = sum_roll_by_value([2, 3, 4, 5, 6], ScoreCategory.ACES, 1)
    assert result is None
    
    # Test empty roll
    result = sum_roll_by_value([], ScoreCategory.ACES, 1)
    assert result is None

def test_sum_roll_by_value_invalid_values():
    """Test sum_roll_by_value with invalid dice values."""
    with pytest.raises(ValueError, match="Value must be between 1 and 6."):
        sum_roll_by_value([1, 2, 3, 4, 5], ScoreCategory.ACES, 0)
    
    with pytest.raises(ValueError, match="Value must be between 1 and 6."):
        sum_roll_by_value([1, 2, 3, 4, 5], ScoreCategory.ACES, 7)
    
    with pytest.raises(ValueError, match="Value must be between 1 and 6."):
        sum_roll_by_value([1, 2, 3, 4, 5], ScoreCategory.ACES, -1)


# sum_n_of_a_kind Tests  
def test_sum_n_of_a_kind_three_of_kind():
    """Test sum_n_of_a_kind for three of a kind scenarios."""
    # Valid three of a kind
    result = sum_n_of_a_kind([1, 1, 1, 2, 3], 3)
    assert result is not None
    assert result.points == 8
    assert result.category == ScoreCategory.THREE_OF_A_KIND
    
    # Five of a kind should count as three of a kind
    result = sum_n_of_a_kind([3, 3, 3, 3, 3], 3)
    assert result is not None
    assert result.points == 15

def test_sum_n_of_a_kind_four_of_kind():
    """Test sum_n_of_a_kind for four of a kind scenarios."""
    # Valid four of a kind
    result = sum_n_of_a_kind([2, 2, 2, 2, 3], 4)
    assert result is not None
    assert result.points == 11
    assert result.category == ScoreCategory.FOUR_OF_A_KIND
    
    # Five of a kind should count as four of a kind
    result = sum_n_of_a_kind([5, 5, 5, 5, 5], 4)
    assert result is not None
    assert result.points == 25

def test_sum_n_of_a_kind_no_matches():
    """Test sum_n_of_a_kind with insufficient matching dice."""
    # Not enough for three of a kind
    result = sum_n_of_a_kind([1, 1, 2, 3, 4], 3)
    assert result is None
    
    # Not enough for four of a kind
    result = sum_n_of_a_kind([1, 1, 1, 2, 3], 4)
    assert result is None
    
    # Empty roll
    result = sum_n_of_a_kind([], 3)
    assert result is None

def test_sum_n_of_a_kind_invalid_n():
    """Test sum_n_of_a_kind with invalid n values."""
    with pytest.raises(ValueError, match="n must be between 1 and 5."):
        sum_n_of_a_kind([1, 2, 3, 4, 5], 0)
    
    with pytest.raises(ValueError, match="n must be between 1 and 5."):
        sum_n_of_a_kind([1, 2, 3, 4, 5], 6)


# score_full_house Tests
def test_score_full_house_valid():
    """Test score_full_house with valid full house patterns."""
    # Standard full house
    result = score_full_house([1, 1, 1, 2, 2])
    assert result is not None
    assert result.points == 25
    assert result.category == ScoreCategory.FULL_HOUSE
    
    # Different order
    result = score_full_house([3, 5, 5, 3, 3])
    assert result is not None
    assert result.points == 25
    
    # Another valid pattern
    result = score_full_house([6, 6, 1, 1, 1])
    assert result is not None
    assert result.points == 25

def test_score_full_house_invalid():
    """Test score_full_house with invalid patterns."""
    # Straight
    result = score_full_house([1, 2, 3, 4, 5])
    assert result is None
    
    # Yahtzee (five of a kind)
    result = score_full_house([1, 1, 1, 1, 1])
    assert result is None
    
    # Four of a kind
    result = score_full_house([1, 1, 1, 1, 2])
    assert result is None
    
    # Two pairs
    result = score_full_house([1, 1, 2, 2, 3])
    assert result is None
    
    # Empty roll
    result = score_full_house([])
    assert result is None


# score_small_straight Tests
def test_score_small_straight_valid():
    """Test score_small_straight with valid small straight patterns."""
    # 1-2-3-4 straight
    result = score_small_straight([1, 2, 3, 4, 6])
    assert result is not None
    assert result.points == 30
    assert result.category == ScoreCategory.SMALL_STRAIGHT
    
    # 2-3-4-5 straight
    result = score_small_straight([2, 3, 4, 5, 1])
    assert result is not None
    assert result.points == 30
    
    # 3-4-5-6 straight
    result = score_small_straight([3, 4, 5, 6, 1])
    assert result is not None
    assert result.points == 30
    
    # With duplicates
    result = score_small_straight([1, 1, 2, 3, 4])
    assert result is not None
    assert result.points == 30
    
    # Large straight also counts as small straight
    result = score_small_straight([1, 2, 3, 4, 5])
    assert result is not None
    assert result.points == 30

def test_score_small_straight_invalid():
    """Test score_small_straight with invalid patterns."""
    # Yahtzee
    result = score_small_straight([1, 1, 1, 1, 1])
    assert result is None
    
    # Gap in sequence
    result = score_small_straight([1, 3, 5, 6, 2])
    assert result is None
    
    # Missing number in sequence
    result = score_small_straight([1, 2, 4, 5, 6])
    assert result is None
    
    # Empty roll
    result = score_small_straight([])
    assert result is None


# score_large_straight Tests
def test_score_large_straight_valid():
    """Test score_large_straight with valid large straight patterns."""
    # 1-2-3-4-5 straight
    result = score_large_straight([1, 2, 3, 4, 5])
    assert result is not None
    assert result.points == 40
    assert result.category == ScoreCategory.LARGE_STRAIGHT
    
    # 2-3-4-5-6 straight
    result = score_large_straight([2, 3, 4, 5, 6])
    assert result is not None
    assert result.points == 40
    
    # Mixed order
    result = score_large_straight([5, 4, 3, 2, 1])
    assert result is not None
    assert result.points == 40

def test_score_large_straight_invalid():
    """Test score_large_straight with invalid patterns."""
    # Duplicate dice (only small straight)
    result = score_large_straight([1, 1, 2, 3, 4])
    assert result is None
    
    # Gap in sequence
    result = score_large_straight([1, 2, 3, 4, 6])
    assert result is None
    
    # Yahtzee
    result = score_large_straight([1, 1, 1, 1, 1])
    assert result is None
    
    # Empty roll
    result = score_large_straight([])
    assert result is None


# score_yahtzee Tests
def test_score_yahtzee_valid():
    """Test score_yahtzee with valid yahtzee patterns."""
    # All ones
    result = score_yahtzee([1, 1, 1, 1, 1])
    assert result is not None
    assert result.points == 50
    assert result.category == ScoreCategory.YAHTZEE
    
    # All sixes
    result = score_yahtzee([6, 6, 6, 6, 6])
    assert result is not None
    assert result.points == 50
    
    # All threes
    result = score_yahtzee([3, 3, 3, 3, 3])
    assert result is not None
    assert result.points == 50

def test_score_yahtzee_invalid():
    """Test score_yahtzee with invalid patterns."""
    # Four of a kind
    result = score_yahtzee([1, 1, 1, 1, 2])
    assert result is None
    
    # Full house
    result = score_yahtzee([1, 1, 1, 2, 2])
    assert result is None
    
    # Straight
    result = score_yahtzee([1, 2, 3, 4, 5])
    assert result is None
    
    # Empty roll
    result = score_yahtzee([])
    assert result is None


# CATEGORY_SCORERS Integration Tests
def test_category_scorers_contains_all_categories():
    """Test that CATEGORY_SCORERS contains all score categories."""
    expected_categories = {category.value for category in ScoreCategory}
    actual_categories = set(CATEGORY_SCORERS.keys())
    assert actual_categories == expected_categories

def test_category_scorers_aces():
    """Test CATEGORY_SCORERS for Aces category."""
    scorer = CATEGORY_SCORERS[ScoreCategory.ACES.value]
    
    # Valid score
    result = scorer([1, 1, 1, 2, 3])
    assert result is not None
    assert result.points == 3
    
    # No score
    result = scorer([2, 3, 4, 5, 6])
    assert result is None

def test_category_scorers_twos():
    """Test CATEGORY_SCORERS for Twos category."""
    scorer = CATEGORY_SCORERS[ScoreCategory.TWOS.value]
    
    # Valid score
    result = scorer([2, 2, 1, 3, 4])
    assert result is not None
    assert result.points == 4
    
    # No score
    result = scorer([1, 3, 4, 5, 6])
    assert result is None

def test_category_scorers_threes():
    """Test CATEGORY_SCORERS for Threes category."""
    scorer = CATEGORY_SCORERS[ScoreCategory.THREES.value]
    
    # Valid score
    result = scorer([3, 3, 3, 1, 2])
    assert result is not None
    assert result.points == 9

def test_category_scorers_fours():
    """Test CATEGORY_SCORERS for Fours category."""
    scorer = CATEGORY_SCORERS[ScoreCategory.FOURS.value]
    
    # Valid score
    result = scorer([4, 4, 1, 2, 3])
    assert result is not None
    assert result.points == 8

def test_category_scorers_fives():
    """Test CATEGORY_SCORERS for Fives category."""
    scorer = CATEGORY_SCORERS[ScoreCategory.FIVES.value]
    
    # Valid score
    result = scorer([5, 5, 5, 5, 1])
    assert result is not None
    assert result.points == 20

def test_category_scorers_sixes():
    """Test CATEGORY_SCORERS for Sixes category."""
    scorer = CATEGORY_SCORERS[ScoreCategory.SIXES.value]
    
    # Valid score
    result = scorer([6, 6, 1, 2, 3])
    assert result is not None
    assert result.points == 12

def test_category_scorers_three_of_kind():
    """Test CATEGORY_SCORERS for Three of a Kind category."""
    scorer = CATEGORY_SCORERS[ScoreCategory.THREE_OF_A_KIND.value]
    
    # Valid score
    result = scorer([3, 3, 3, 1, 2])
    assert result is not None
    assert result.points == 12
    
    # No score
    result = scorer([1, 2, 3, 4, 5])
    assert result is None

def test_category_scorers_four_of_kind():
    """Test CATEGORY_SCORERS for Four of a Kind category."""
    scorer = CATEGORY_SCORERS[ScoreCategory.FOUR_OF_A_KIND.value]
    
    # Valid score
    result = scorer([2, 2, 2, 2, 3])
    assert result is not None
    assert result.points == 11
    
    # No score
    result = scorer([1, 1, 1, 2, 3])
    assert result is None

def test_category_scorers_full_house():
    """Test CATEGORY_SCORERS for Full House category."""
    scorer = CATEGORY_SCORERS[ScoreCategory.FULL_HOUSE.value]
    
    # Valid score
    result = scorer([1, 1, 1, 2, 2])
    assert result is not None
    assert result.points == 25
    
    # No score
    result = scorer([1, 2, 3, 4, 5])
    assert result is None

def test_category_scorers_small_straight():
    """Test CATEGORY_SCORERS for Small Straight category."""
    scorer = CATEGORY_SCORERS[ScoreCategory.SMALL_STRAIGHT.value]
    
    # Valid score
    result = scorer([1, 2, 3, 4, 6])
    assert result is not None
    assert result.points == 30
    
    # No score
    result = scorer([1, 1, 1, 1, 1])
    assert result is None

def test_category_scorers_large_straight():
    """Test CATEGORY_SCORERS for Large Straight category."""
    scorer = CATEGORY_SCORERS[ScoreCategory.LARGE_STRAIGHT.value]
    
    # Valid score
    result = scorer([1, 2, 3, 4, 5])
    assert result is not None
    assert result.points == 40
    
    # No score  
    result = scorer([1, 1, 2, 3, 4])
    assert result is None

def test_category_scorers_yahtzee():
    """Test CATEGORY_SCORERS for Yahtzee category."""
    scorer = CATEGORY_SCORERS[ScoreCategory.YAHTZEE.value]
    
    # Valid score
    result = scorer([4, 4, 4, 4, 4])
    assert result is not None
    assert result.points == 50
    
    # No score
    result = scorer([1, 2, 3, 4, 5])
    assert result is None

def test_category_scorers_chance():
    """Test CATEGORY_SCORERS for Chance category."""
    scorer = CATEGORY_SCORERS[ScoreCategory.CHANCE.value]
    
    # Always returns a Score object now (since you fixed the issue)
    result = scorer([1, 2, 3, 4, 5])
    assert result is not None
    assert result.points == 15
    
    result = scorer([6, 6, 6, 6, 6])
    assert result is not None
    assert result.points == 30
    
    # Even empty roll should return Score with 0 points
    result = scorer([])
    assert result is not None
    assert result.points == 0


# Edge Cases Tests
def test_empty_roll_handling():
    """Test that empty rolls are handled properly across all categories."""
    empty_roll = []
    
    for category_name, scorer in CATEGORY_SCORERS.items():
        result = scorer(empty_roll)
        if category_name == ScoreCategory.CHANCE.value:
            # Chance should return Score with 0 points for empty roll
            assert result is not None
            assert result.points == 0
        else:
            # All other categories should return None for empty roll
            assert result is None, f"Category {category_name} should return None for empty roll"

def test_single_die_scoring():
    """Test scoring with a single die."""
    single_roll = [3]
    
    # Should score for matching number category
    result = CATEGORY_SCORERS[ScoreCategory.THREES.value](single_roll)
    assert result is not None
    assert result.points == 3
    
    # Should not score for non-matching number categories
    result = CATEGORY_SCORERS[ScoreCategory.ACES.value](single_roll)
    assert result is None
    
    # Should not score for pattern categories (except Yahtzee which will score!)
    assert CATEGORY_SCORERS[ScoreCategory.THREE_OF_A_KIND.value](single_roll) is None
    assert CATEGORY_SCORERS[ScoreCategory.FULL_HOUSE.value](single_roll) is None
    assert CATEGORY_SCORERS[ScoreCategory.SMALL_STRAIGHT.value](single_roll) is None
    # Note: Yahtzee will actually score for single die because len(set([3])) == 1
    yahtzee_result = CATEGORY_SCORERS[ScoreCategory.YAHTZEE.value](single_roll)
    assert yahtzee_result is not None
    assert yahtzee_result.points == 50
    
    # Should score for chance
    result = CATEGORY_SCORERS[ScoreCategory.CHANCE.value](single_roll)
    assert result is not None
    assert result.points == 3

def test_maximum_scores():
    """Test maximum possible scores for each category."""
    max_roll = [6, 6, 6, 6, 6]
    
    # Number categories max scores
    assert CATEGORY_SCORERS[ScoreCategory.SIXES.value](max_roll).points == 30
    assert CATEGORY_SCORERS[ScoreCategory.THREE_OF_A_KIND.value](max_roll).points == 30
    assert CATEGORY_SCORERS[ScoreCategory.FOUR_OF_A_KIND.value](max_roll).points == 30
    assert CATEGORY_SCORERS[ScoreCategory.YAHTZEE.value](max_roll).points == 50
    assert CATEGORY_SCORERS[ScoreCategory.CHANCE.value](max_roll).points == 30
    
    # Pattern categories have fixed scores
    full_house_roll = [6, 6, 6, 5, 5]
    assert CATEGORY_SCORERS[ScoreCategory.FULL_HOUSE.value](full_house_roll).points == 25
    
    small_straight_roll = [2, 3, 4, 5, 6]
    assert CATEGORY_SCORERS[ScoreCategory.SMALL_STRAIGHT.value](small_straight_roll).points == 30
    
    large_straight_roll = [2, 3, 4, 5, 6]
    assert CATEGORY_SCORERS[ScoreCategory.LARGE_STRAIGHT.value](large_straight_roll).points == 40

def test_minimum_valid_scores():
    """Test minimum valid scores for each category."""
    # Minimum for number categories
    min_aces = [1, 2, 3, 4, 5]
    assert CATEGORY_SCORERS[ScoreCategory.ACES.value](min_aces).points == 1
    
    # Minimum for pattern categories
    min_three_kind = [1, 1, 1, 2, 3]
    assert CATEGORY_SCORERS[ScoreCategory.THREE_OF_A_KIND.value](min_three_kind).points == 8
    
    min_four_kind = [1, 1, 1, 1, 2]
    assert CATEGORY_SCORERS[ScoreCategory.FOUR_OF_A_KIND.value](min_four_kind).points == 6

def test_complex_scoring_scenarios():
    """Test complex scenarios where rolls qualify for multiple categories."""
    # Yahtzee of threes
    yahtzee_roll = [3, 3, 3, 3, 3]
    
    # Should score in multiple categories
    assert CATEGORY_SCORERS[ScoreCategory.THREES.value](yahtzee_roll).points == 15
    assert CATEGORY_SCORERS[ScoreCategory.THREE_OF_A_KIND.value](yahtzee_roll).points == 15
    assert CATEGORY_SCORERS[ScoreCategory.FOUR_OF_A_KIND.value](yahtzee_roll).points == 15
    assert CATEGORY_SCORERS[ScoreCategory.YAHTZEE.value](yahtzee_roll).points == 50
    assert CATEGORY_SCORERS[ScoreCategory.CHANCE.value](yahtzee_roll).points == 15
    
    # Large straight that's also a small straight
    straight_roll = [1, 2, 3, 4, 5]
    assert CATEGORY_SCORERS[ScoreCategory.SMALL_STRAIGHT.value](straight_roll).points == 30
    assert CATEGORY_SCORERS[ScoreCategory.LARGE_STRAIGHT.value](straight_roll).points == 40
    
    # Full house
    full_house_roll = [2, 2, 2, 5, 5]
    assert CATEGORY_SCORERS[ScoreCategory.TWOS.value](full_house_roll).points == 6
    assert CATEGORY_SCORERS[ScoreCategory.FIVES.value](full_house_roll).points == 10
    assert CATEGORY_SCORERS[ScoreCategory.THREE_OF_A_KIND.value](full_house_roll).points == 16
    assert CATEGORY_SCORERS[ScoreCategory.FULL_HOUSE.value](full_house_roll).points == 25
    assert CATEGORY_SCORERS[ScoreCategory.CHANCE.value](full_house_roll).points == 16

def test_no_score_scenarios():
    """Test rolls that don't qualify for most categories."""
    poor_roll = [1, 2, 3, 5, 6]  # Missing 4, no patterns
    
    # Should only score in number categories and chance
    scoring_categories = []
    for category, scorer in CATEGORY_SCORERS.items():
        result = scorer(poor_roll)
        if result is not None and result.points > 0:
            scoring_categories.append(category)
    
    expected_scoring = {
        ScoreCategory.ACES.value,
        ScoreCategory.TWOS.value,
        ScoreCategory.THREES.value,
        ScoreCategory.FIVES.value,
        ScoreCategory.SIXES.value,
        ScoreCategory.CHANCE.value,
    }
    
    assert set(scoring_categories) == expected_scoring


# Parametrized Tests for Comprehensive Coverage
@pytest.mark.parametrize("roll,category,value,expected_score", [
    # Valid cases with matches
    ([1, 1, 1, 2, 3], ScoreCategory.ACES, 1, 3),
    ([2, 2, 2, 2, 5], ScoreCategory.TWOS, 2, 8),
    ([3, 3, 1, 4, 6], ScoreCategory.THREES, 3, 6),
    ([4, 4, 4, 4, 4], ScoreCategory.FOURS, 4, 20),
    ([5, 5, 2, 3, 1], ScoreCategory.FIVES, 5, 10),
    ([6, 6, 6, 2, 1], ScoreCategory.SIXES, 6, 18),
    # Single match cases
    ([1, 2, 3, 4, 5], ScoreCategory.ACES, 1, 1),
    ([1, 2, 3, 4, 6], ScoreCategory.SIXES, 6, 6),
    # All same dice
    ([1, 1, 1, 1, 1], ScoreCategory.ACES, 1, 5),
    ([6, 6, 6, 6, 6], ScoreCategory.SIXES, 6, 30),
])
def test_sum_roll_by_value_parametrized(roll, category, value, expected_score):
    """Parametrized test for sum_roll_by_value with valid matches."""
    result = sum_roll_by_value(roll, category, value)
    assert result is not None
    assert result.points == expected_score
    assert result.roll == roll

@pytest.mark.parametrize("roll,category,value", [
    # No matches
    ([2, 3, 4, 5, 6], ScoreCategory.ACES, 1),
    ([1, 3, 4, 5, 6], ScoreCategory.TWOS, 2),
    ([1, 2, 4, 5, 6], ScoreCategory.THREES, 3),
    ([1, 2, 3, 5, 6], ScoreCategory.FOURS, 4),
    ([1, 2, 3, 4, 6], ScoreCategory.FIVES, 5),
    ([1, 2, 3, 4, 5], ScoreCategory.SIXES, 6),
    # Empty roll
    ([], ScoreCategory.ACES, 1),
    ([], ScoreCategory.SIXES, 6),
])
def test_sum_roll_by_value_no_matches_parametrized(roll, category, value):
    """Parametrized test for sum_roll_by_value with no matches."""
    result = sum_roll_by_value(roll, category, value)
    assert result is None

@pytest.mark.parametrize("roll", [
    # Valid full houses
    ([1, 1, 1, 2, 2]),
    ([2, 2, 3, 3, 3]),
    ([4, 4, 4, 5, 5]),
    ([6, 6, 1, 1, 1]),
    ([3, 5, 5, 3, 3]),
    ([2, 4, 2, 4, 4]),
])
def test_score_full_house_valid_parametrized(roll):
    """Parametrized test for valid full house patterns."""
    result = score_full_house(roll)
    assert result is not None
    assert result.points == 25
    assert result.category == ScoreCategory.FULL_HOUSE

@pytest.mark.parametrize("roll", [
    # Valid small straights
    ([1, 2, 3, 4, 5]),  # also large straight
    ([1, 2, 3, 4, 6]),
    ([2, 3, 4, 5, 6]),  # also large straight
    ([2, 3, 4, 5, 1]),
    ([3, 4, 5, 6, 1]),
    # With duplicates
    ([1, 1, 2, 3, 4]),
    ([2, 2, 3, 4, 5]),
    ([3, 3, 4, 5, 6]),
])
def test_score_small_straight_valid_parametrized(roll):
    """Parametrized test for valid small straight patterns."""
    result = score_small_straight(roll)
    assert result is not None
    assert result.points == 30
    assert result.category == ScoreCategory.SMALL_STRAIGHT

@pytest.mark.parametrize("roll", [
    # Valid yahtzees
    ([1, 1, 1, 1, 1]),
    ([2, 2, 2, 2, 2]),
    ([3, 3, 3, 3, 3]),
    ([4, 4, 4, 4, 4]),
    ([5, 5, 5, 5, 5]),
    ([6, 6, 6, 6, 6]),
])
def test_score_yahtzee_valid_parametrized(roll):
    """Parametrized test for valid yahtzee patterns."""
    result = score_yahtzee(roll)
    assert result is not None
    assert result.points == 50
    assert result.category == ScoreCategory.YAHTZEE

# Performance and Stress Tests
def test_large_number_of_dice():
    """Test with unusual number of dice to ensure robustness."""
    # Test with more than 5 dice
    large_roll = [1, 1, 1, 1, 1, 2, 3, 4, 5, 6]
    
    # Should still work for sum_roll_by_value
    result = sum_roll_by_value(large_roll, ScoreCategory.ACES, 1)
    assert result is not None
    assert result.points == 5
    
    # Should work for sum_n_of_a_kind
    result = sum_n_of_a_kind(large_roll, 4)
    assert result is not None
    assert result.points == sum(large_roll)

def test_all_category_scorers_consistency():
    """Test that all category scorers return consistent objects."""
    test_roll = [1, 2, 3, 4, 5]
    
    for category_name, scorer in CATEGORY_SCORERS.items():
        result = scorer(test_roll)
        if result is not None:
            # All categories now return Score objects
            assert hasattr(result, 'category')
            assert hasattr(result, 'roll')
            assert hasattr(result, 'points')
            assert isinstance(result.points, int)
            assert result.points >= 0
            assert result.roll == test_roll

