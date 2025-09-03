import pytest

from src.scorer import Scorer
from src.score import Score
from src.score_category import ScoreCategory


# Scorer class initialization tests
def test_scorer_initialization():
    """Test that Scorer initializes correctly with category scorers."""
    scorer = Scorer()
    assert scorer._category_scorers is not None
    assert len(scorer._category_scorers) == len(ScoreCategory)
    assert scorer._min_dice == 5  # Test default min_dice value
    
    # Verify all categories are present
    expected_categories = {category.value for category in ScoreCategory}
    actual_categories = set(scorer._category_scorers.keys())
    assert actual_categories == expected_categories


def test_scorer_initialization_custom_min_dice():
    """Test that Scorer can be initialized with custom min_dice value."""
    scorer = Scorer(min_dice=3)
    assert scorer._min_dice == 3
    
    scorer = Scorer(min_dice=1)
    assert scorer._min_dice == 1


# Basic get_scores functionality tests
def test_get_scores_returns_list():
    """Test that get_scores returns a list."""
    scorer = Scorer()
    result = scorer.get_scores([1, 2, 3, 4, 5])
    assert isinstance(result, list)


def test_get_scores_returns_score_objects():
    """Test that get_scores returns Score objects."""
    scorer = Scorer()
    result = scorer.get_scores([1, 1, 1, 1, 1])  # Yahtzee of 1s
    assert len(result) > 0
    
    for score in result:
        assert isinstance(score, Score)
        assert hasattr(score, 'category')
        assert hasattr(score, 'roll')
        assert hasattr(score, 'points')


def test_get_scores_empty_roll():
    """Test get_scores with empty roll."""
    scorer = Scorer()
    result = scorer.get_scores([])
    
    # With min_dice=5, empty roll should return no scores
    assert len(result) == 0
    assert result == []


def test_get_scores_insufficient_dice():
    """Test get_scores with insufficient dice."""
    scorer = Scorer()
    
    # Test with 1-4 dice (less than minimum 5)
    for num_dice in range(1, 5):
        roll = [1] * num_dice
        result = scorer.get_scores(roll)
        assert len(result) == 0, f"Expected no scores for {num_dice} dice"


def test_get_scores_custom_min_dice():
    """Test get_scores with custom min_dice setting."""
    # Test with min_dice=1 to allow single die scoring
    scorer = Scorer(min_dice=1)
    
    # Single die should now score
    result = scorer.get_scores([3])
    assert len(result) > 0
    categories = {score.category for score in result}
    assert ScoreCategory.THREES in categories
    assert ScoreCategory.YAHTZEE in categories
    assert ScoreCategory.CHANCE in categories
    
    # Empty roll with min_dice=0
    scorer_zero = Scorer(min_dice=0)
    result = scorer_zero.get_scores([])
    assert len(result) == 1  # Should get Chance
    assert result[0].category == ScoreCategory.CHANCE
    assert result[0].points == 0


# Data-driven tests for specific roll patterns
@pytest.mark.parametrize("roll,expected_categories", [
    # Yahtzee - should score in multiple categories
    ([1, 1, 1, 1, 1], {
        ScoreCategory.ACES,
        ScoreCategory.THREE_OF_A_KIND,
        ScoreCategory.FOUR_OF_A_KIND,
        ScoreCategory.YAHTZEE,
        ScoreCategory.CHANCE
    }),
    ([6, 6, 6, 6, 6], {
        ScoreCategory.SIXES,
        ScoreCategory.THREE_OF_A_KIND,
        ScoreCategory.FOUR_OF_A_KIND,
        ScoreCategory.YAHTZEE,
        ScoreCategory.CHANCE
    }),
    
    # Large straight - should also count as small straight
    ([1, 2, 3, 4, 5], {
        ScoreCategory.ACES,
        ScoreCategory.TWOS,
        ScoreCategory.THREES,
        ScoreCategory.FOURS,
        ScoreCategory.FIVES,
        ScoreCategory.SMALL_STRAIGHT,
        ScoreCategory.LARGE_STRAIGHT,
        ScoreCategory.CHANCE
    }),
    ([2, 3, 4, 5, 6], {
        ScoreCategory.TWOS,
        ScoreCategory.THREES,
        ScoreCategory.FOURS,
        ScoreCategory.FIVES,
        ScoreCategory.SIXES,
        ScoreCategory.SMALL_STRAIGHT,
        ScoreCategory.LARGE_STRAIGHT,
        ScoreCategory.CHANCE
    }),
    
    # Full house
    ([1, 1, 1, 2, 2], {
        ScoreCategory.ACES,
        ScoreCategory.TWOS,
        ScoreCategory.THREE_OF_A_KIND,
        ScoreCategory.FULL_HOUSE,
        ScoreCategory.CHANCE
    }),
    ([3, 3, 5, 5, 5], {
        ScoreCategory.THREES,
        ScoreCategory.FIVES,
        ScoreCategory.THREE_OF_A_KIND,
        ScoreCategory.FULL_HOUSE,
        ScoreCategory.CHANCE
    }),
    
    # Four of a kind
    ([2, 2, 2, 2, 3], {
        ScoreCategory.TWOS,
        ScoreCategory.THREES,
        ScoreCategory.THREE_OF_A_KIND,
        ScoreCategory.FOUR_OF_A_KIND,
        ScoreCategory.CHANCE
    }),
    
    # Three of a kind only
    ([4, 4, 4, 1, 6], {
        ScoreCategory.ACES,
        ScoreCategory.FOURS,
        ScoreCategory.SIXES,
        ScoreCategory.THREE_OF_A_KIND,
        ScoreCategory.CHANCE
    }),
    
    # Small straight only (with duplicate)
    ([1, 2, 3, 4, 4], {
        ScoreCategory.ACES,
        ScoreCategory.TWOS,
        ScoreCategory.THREES,
        ScoreCategory.FOURS,
        ScoreCategory.SMALL_STRAIGHT,
        ScoreCategory.CHANCE
    }),
    
    # No special patterns (only number categories and chance)
    ([1, 2, 3, 5, 6], {
        ScoreCategory.ACES,
        ScoreCategory.TWOS,
        ScoreCategory.THREES,
        ScoreCategory.FIVES,
        ScoreCategory.SIXES,
        ScoreCategory.CHANCE
    }),
])
def test_get_scores_expected_categories(roll, expected_categories):
    """Test that get_scores returns expected categories for specific rolls."""
    scorer = Scorer()
    result = scorer.get_scores(roll)
    
    actual_categories = {score.category for score in result}
    assert actual_categories == expected_categories


def test_get_scores_expected_categories_insufficient_dice():
    """Test that get_scores returns empty list for insufficient dice."""
    scorer = Scorer()
    
    # Test single die - should return empty with default min_dice=5
    result = scorer.get_scores([3])
    assert len(result) == 0
    assert result == []
    
    # Test empty roll - should return empty with default min_dice=5
    result = scorer.get_scores([])
    assert len(result) == 0
    assert result == []
    
    # Test with custom min_dice to allow single die scoring
    scorer_custom = Scorer(min_dice=1)
    result = scorer_custom.get_scores([3])
    expected_categories = {
        ScoreCategory.THREES,
        ScoreCategory.YAHTZEE,  # Single die counts as Yahtzee
        ScoreCategory.CHANCE
    }
    actual_categories = {score.category for score in result}
    assert actual_categories == expected_categories


@pytest.mark.parametrize("roll,category,expected_points", [
    # Test specific point values for different rolls and categories
    ([1, 1, 1, 2, 3], ScoreCategory.ACES, 3),
    ([1, 1, 1, 2, 3], ScoreCategory.TWOS, 2),
    ([1, 1, 1, 2, 3], ScoreCategory.THREE_OF_A_KIND, 8),
    ([1, 1, 1, 2, 3], ScoreCategory.CHANCE, 8),
    
    ([6, 6, 6, 6, 6], ScoreCategory.SIXES, 30),
    ([6, 6, 6, 6, 6], ScoreCategory.YAHTZEE, 50),
    ([6, 6, 6, 6, 6], ScoreCategory.CHANCE, 30),
    
    ([1, 2, 3, 4, 5], ScoreCategory.SMALL_STRAIGHT, 30),
    ([1, 2, 3, 4, 5], ScoreCategory.LARGE_STRAIGHT, 40),
    ([1, 2, 3, 4, 5], ScoreCategory.CHANCE, 15),
    
    ([2, 2, 2, 5, 5], ScoreCategory.FULL_HOUSE, 25),
    ([2, 2, 2, 5, 5], ScoreCategory.THREE_OF_A_KIND, 16),
    ([2, 2, 2, 5, 5], ScoreCategory.TWOS, 6),
    ([2, 2, 2, 5, 5], ScoreCategory.FIVES, 10),
])
def test_get_scores_specific_points(roll, category, expected_points):
    """Test that get_scores returns correct point values."""
    scorer = Scorer()
    result = scorer.get_scores(roll)
    
    # Find the score for the specified category
    category_score = next((score for score in result if score.category == category), None)
    assert category_score is not None, f"Expected {category} to be in results"
    assert category_score.points == expected_points


@pytest.mark.parametrize("roll,expected_count", [
    # Test expected number of scoring categories (only 5+ dice rolls)
    ([1, 1, 1, 1, 1], 5),  # Aces, 3-kind, 4-kind, Yahtzee, Chance
    ([1, 2, 3, 4, 5], 8),   # All numbers, small straight, large straight, chance
    ([2, 3, 4, 5, 6], 8),   # All numbers, small straight, large straight, chance
    ([1, 1, 1, 2, 2], 5),   # Aces, Twos, 3-kind, Full house, Chance
    ([2, 2, 2, 2, 3], 5),   # Twos, Threes, 3-kind, 4-kind, Chance
    ([1, 2, 3, 5, 6], 6),   # Five number categories + Chance
])
def test_get_scores_count(roll, expected_count):
    """Test that get_scores returns expected number of scores."""
    scorer = Scorer()
    result = scorer.get_scores(roll)
    assert len(result) == expected_count


def test_get_scores_count_insufficient_dice():
    """Test that get_scores returns 0 for insufficient dice."""
    scorer = Scorer()
    
    # Test rolls with < 5 dice should return 0 scores
    test_cases = [
        ([3], 0),        # Single die
        ([], 0),         # Empty roll
        ([1, 2], 0),     # Two dice
        ([1, 2, 3], 0),  # Three dice
        ([1, 2, 3, 4], 0) # Four dice
    ]
    
    for roll, expected_count in test_cases:
        result = scorer.get_scores(roll)
        assert len(result) == expected_count, f"Expected {expected_count} scores for roll {roll}, got {len(result)}"


def test_get_scores_count_custom_min_dice():
    """Test get_scores count with custom min_dice values."""
    # Test with min_dice=1
    scorer = Scorer(min_dice=1)
    result = scorer.get_scores([3])  # Single die
    assert len(result) == 3  # Threes, Yahtzee, Chance
    
    # Test with min_dice=0  
    scorer = Scorer(min_dice=0)
    result = scorer.get_scores([])  # Empty roll
    assert len(result) == 1  # Only Chance


# Data-driven tests for insufficient dice cases
@pytest.mark.parametrize("roll", [
    [3],        # Single die
    [],         # Empty roll
    [1, 2],     # Two dice
    [1, 2, 3],  # Three dice
    [1, 2, 3, 4] # Four dice
])
def test_get_scores_insufficient_dice_cases(roll):
    """Test that get_scores returns no scores for insufficient dice."""
    scorer = Scorer()
    result = scorer.get_scores(roll)
    assert len(result) == 0


# Edge case tests
def test_get_scores_all_different_dice():
    """Test get_scores with all different dice values."""
    scorer = Scorer()
    
    # Should only score in number categories and chance (no patterns)
    # Note: [1,2,3,4,6] actually contains a small straight [1,2,3,4]
    result = scorer.get_scores([1, 2, 3, 4, 6])
    expected_categories = {
        ScoreCategory.ACES,
        ScoreCategory.TWOS,
        ScoreCategory.THREES,
        ScoreCategory.FOURS,
        ScoreCategory.SIXES,
        ScoreCategory.SMALL_STRAIGHT,  # [1,2,3,4] forms a small straight
        ScoreCategory.CHANCE
    }
    
    actual_categories = {score.category for score in result}
    assert actual_categories == expected_categories


def test_get_scores_maximum_possible():
    """Test get_scores with roll that maximizes scoring categories."""
    scorer = Scorer()
    
    # Yahtzee of 6s should score in many categories
    result = scorer.get_scores([6, 6, 6, 6, 6])
    
    # Should have high total points
    total_points = sum(score.points for score in result)
    assert total_points > 100  # 30 + 30 + 30 + 50 + 30 = 170


def test_get_scores_minimum_possible():
    """Test get_scores with roll that minimizes scoring categories."""
    scorer = Scorer()
    
    # Roll with minimal scoring opportunities - avoid consecutive numbers
    result = scorer.get_scores([1, 2, 4, 6, 6])
    
    # Should only have number categories and chance
    categories = {score.category for score in result}
    assert ScoreCategory.FULL_HOUSE not in categories
    assert ScoreCategory.THREE_OF_A_KIND not in categories
    assert ScoreCategory.SMALL_STRAIGHT not in categories


# Test roll validation and edge cases
def test_get_scores_large_roll():
    """Test get_scores with more than 5 dice."""
    scorer = Scorer()
    
    # Should still work with extra dice but won't be Yahtzee due to mixed values
    result = scorer.get_scores([1, 1, 1, 1, 1, 2, 3])
    
    # Should still detect some patterns but not Yahtzee (mixed values)
    categories = {score.category for score in result}
    assert ScoreCategory.FOUR_OF_A_KIND in categories  # Has at least 4 ones
    assert ScoreCategory.THREE_OF_A_KIND in categories  # Has at least 3 ones
    assert ScoreCategory.ACES in categories
    # Yahtzee requires all dice to be the same, which this roll doesn't satisfy


def test_get_scores_single_category_multiple_times():
    """Test that each category appears at most once in results."""
    scorer = Scorer()
    
    result = scorer.get_scores([1, 1, 1, 1, 1])
    
    # Count occurrences of each category
    category_counts = {}
    for score in result:
        category_counts[score.category] = category_counts.get(score.category, 0) + 1
    
    # Each category should appear exactly once
    for category, count in category_counts.items():
        assert count == 1, f"Category {category} appears {count} times"


# Test that all scores have correct roll data
def test_get_scores_roll_consistency():
    """Test that all returned scores have correct roll data."""
    scorer = Scorer()
    test_roll = [2, 2, 2, 5, 5]
    
    result = scorer.get_scores(test_roll)
    
    for score in result:
        assert score.roll == test_roll, f"Score {score.category} has incorrect roll data"


# Comprehensive integration tests
@pytest.mark.parametrize("roll", [
    [1, 1, 1, 1, 1],  # Yahtzee of 1s
    [2, 3, 4, 5, 6],  # Large straight
    [3, 3, 3, 5, 5],  # Full house
    [4, 4, 4, 4, 1],  # Four of a kind
    [1, 2, 3, 4, 4],  # Small straight with duplicate
    [6, 6, 1, 2, 3],  # Mixed numbers
    [5, 5, 5, 2, 1],  # Three of a kind
    [1, 2, 3, 5, 6],  # No patterns
    [3],              # Single die
    [],               # Empty roll
])
def test_get_scores_comprehensive(roll):
    """Comprehensive test that scores are valid for various rolls."""
    scorer = Scorer()
    result = scorer.get_scores(roll)
    
    # Basic validations
    assert isinstance(result, list)
    
    for score in result:
        # Each result should be a valid Score object
        assert isinstance(score, Score)
        assert isinstance(score.category, ScoreCategory)
        assert isinstance(score.points, int)
        assert score.points >= 0
        assert score.roll == roll
        
        # Points should be reasonable (not negative, not impossibly high)
        assert score.points <= 300  # Arbitrary upper bound


def test_get_scores_deterministic():
    """Test that get_scores returns consistent results for same input."""
    scorer = Scorer()
    roll = [1, 2, 3, 4, 5]
    
    result1 = scorer.get_scores(roll)
    result2 = scorer.get_scores(roll)
    
    # Should get same number of scores
    assert len(result1) == len(result2)
    
    # Convert to sets for comparison (order might vary)
    scores1 = {(score.category, score.points) for score in result1}
    scores2 = {(score.category, score.points) for score in result2}
    
    assert scores1 == scores2


def test_scorer_multiple_instances():
    """Test that multiple Scorer instances behave consistently."""
    scorer1 = Scorer()
    scorer2 = Scorer()
    
    test_roll = [3, 3, 3, 6, 6]
    
    result1 = scorer1.get_scores(test_roll)
    result2 = scorer2.get_scores(test_roll)
    
    # Results should be identical
    assert len(result1) == len(result2)
    
    scores1 = {(score.category, score.points) for score in result1}
    scores2 = {(score.category, score.points) for score in result2}
    
    assert scores1 == scores2


# Performance and stress tests
def test_get_scores_performance():
    """Basic performance test - should handle typical rolls quickly."""
    scorer = Scorer()
    
    # Test with various roll patterns
    test_rolls = [
        [1, 1, 1, 1, 1],
        [1, 2, 3, 4, 5],
        [2, 2, 2, 5, 5],
        [6, 6, 6, 6, 1],
        [1, 2, 3, 5, 6]
    ]
    
    for roll in test_rolls:
        result = scorer.get_scores(roll)
        assert len(result) > 0  # Should always return at least chance


def test_get_scores_all_scoring_scenarios():
    """Test that scorer can handle all major Yahtzee scoring scenarios."""
    scorer = Scorer()
    
    scenarios = [
        # Each major pattern type
        ([1, 1, 1, 1, 1], "Yahtzee"),
        ([1, 2, 3, 4, 5], "Large Straight"),
        ([2, 3, 4, 5, 6], "Large Straight 2"),
        ([1, 2, 3, 4, 6], "Small Straight"),
        ([2, 2, 2, 5, 5], "Full House"),
        ([3, 3, 3, 3, 1], "Four of a Kind"),
        ([4, 4, 4, 2, 6], "Three of a Kind"),
        ([1, 2, 3, 5, 6], "No Pattern"),
    ]
    
    for roll, description in scenarios:
        result = scorer.get_scores(roll)
        assert len(result) > 0, f"No scores for {description}: {roll}"
        
        # Chance should always be present (except for empty roll case)
        if roll:  # Non-empty roll
            categories = {score.category for score in result}
            assert ScoreCategory.CHANCE in categories, f"Missing Chance for {description}"
