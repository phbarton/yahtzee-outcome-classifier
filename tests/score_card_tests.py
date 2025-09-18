import pytest

from src.score_card import ScoreCard
from src.score import Score
from src.score_category import ScoreCategory


# Initialization Tests
def test_default_initialization():
    """Test default initialization of ScoreCard."""
    card = ScoreCard()
    assert len(card.scores) == 13  # All score categories
    assert all(score is None for score in card.scores.values())
    assert card.upper_section_bonus_awarded is False
    assert card.yahtzee_bonus_count == 0


# Available Categories Tests
def test_available_categories_initial():
    """Test that all categories are initially available."""
    card = ScoreCard()
    available = card.available_categories()
    assert len(available) == 13
    assert set(available) == set(ScoreCategory)


def test_available_categories_after_assignments():
    """Test available categories decrease as scores are assigned."""
    card = ScoreCard()
    score = Score(ScoreCategory.ACES, [1, 1, 1, 2, 3], 3)
    card.assign_score(score)
    
    available = card.available_categories()
    assert len(available) == 12
    assert ScoreCategory.ACES not in available


# Assign Score Tests
def test_assign_score_basic():
    """Test basic score assignment."""
    card = ScoreCard()
    score = Score(ScoreCategory.ACES, [1, 1, 1, 2, 3], 3)
    card.assign_score(score)
    
    assert card.get_score(ScoreCategory.ACES) == score


def test_assign_score_duplicate_category():
    """Test that assigning to same category twice raises ValueError."""
    card = ScoreCard()
    score1 = Score(ScoreCategory.ACES, [1, 1, 1, 2, 3], 3)
    score2 = Score(ScoreCategory.ACES, [1, 1, 2, 3, 4], 2)
    
    card.assign_score(score1)
    with pytest.raises(ValueError, match="Category .* has already been scored"):
        card.assign_score(score2)


# Get Score Tests
def test_get_score_assigned():
    """Test getting a score that has been assigned."""
    card = ScoreCard()
    score = Score(ScoreCategory.TWOS, [2, 2, 3, 4, 5], 4)
    card.assign_score(score)
    
    retrieved_score = card.get_score(ScoreCategory.TWOS)
    assert retrieved_score == score


def test_get_score_unassigned():
    """Test getting a score that has not been assigned."""
    card = ScoreCard()
    score = card.get_score(ScoreCategory.ACES)
    assert score is None


# Is Yahtzee Tests
@pytest.mark.parametrize("roll,expected", [
    ([1, 1, 1, 1, 1], True),
    ([2, 2, 2, 2, 2], True),
    ([6, 6, 6, 6, 6], True),
    ([1, 1, 1, 1, 2], False),
    ([1, 2, 3, 4, 5], False),
    ([2, 2, 2, 2], False),  # Not 5 dice
    ([1, 1, 1, 1, 1, 1], False),  # Too many dice
    ([], False),  # Empty roll
])
def test_is_yahtzee(roll, expected):
    """Test the is_yahtzee static method with various rolls."""
    assert ScoreCard.is_yahtzee(roll) == expected


# Yahtzee Bonus Tests
def test_yahtzee_bonus_basic():
    """Test basic Yahtzee bonus functionality."""
    card = ScoreCard()
    
    # First assign regular Yahtzee
    yahtzee_score = Score(ScoreCategory.YAHTZEE, [5, 5, 5, 5, 5], 50)
    card.assign_score(yahtzee_score)
    
    # Then assign another Yahtzee roll to different category
    chance_score = Score(ScoreCategory.CHANCE, [6, 6, 6, 6, 6], 30)
    card.assign_score(chance_score)
    
    assert card.yahtzee_bonus_count == 1


def test_yahtzee_bonus_multiple():
    """Test multiple Yahtzee bonuses."""
    card = ScoreCard()
    
    # First assign regular Yahtzee
    yahtzee_score = Score(ScoreCategory.YAHTZEE, [5, 5, 5, 5, 5], 50)
    card.assign_score(yahtzee_score)
    
    # Assign multiple additional Yahtzee rolls
    chance_score = Score(ScoreCategory.CHANCE, [6, 6, 6, 6, 6], 30)
    card.assign_score(chance_score)
    
    fours_score = Score(ScoreCategory.FOURS, [4, 4, 4, 4, 4], 20)
    card.assign_score(fours_score)
    
    assert card.yahtzee_bonus_count == 2


def test_yahtzee_bonus_no_original_yahtzee():
    """Test that Yahtzee bonus doesn't apply without original Yahtzee."""
    card = ScoreCard()
    
    # Assign Yahtzee roll to chance without filling Yahtzee category
    chance_score = Score(ScoreCategory.CHANCE, [6, 6, 6, 6, 6], 30)
    card.assign_score(chance_score)
    
    assert card.yahtzee_bonus_count == 0


def test_yahtzee_bonus_same_category():
    """Test that Yahtzee bonus doesn't apply when assigning to Yahtzee category."""
    card = ScoreCard()
    
    # Assign Yahtzee roll to Yahtzee category
    yahtzee_score = Score(ScoreCategory.YAHTZEE, [5, 5, 5, 5, 5], 50)
    card.assign_score(yahtzee_score)
    
    assert card.yahtzee_bonus_count == 0


# Upper Section Bonus Tests
@pytest.mark.parametrize("scores,expected_bonus", [
    # Bonus achieved
    ([
        Score(ScoreCategory.ACES, [1, 1, 1, 1, 1], 5),
        Score(ScoreCategory.TWOS, [2, 2, 2, 2, 2], 10),
        Score(ScoreCategory.THREES, [3, 3, 3, 3, 3], 15),
        Score(ScoreCategory.FOURS, [4, 4, 4, 4, 4], 20),
        Score(ScoreCategory.FIVES, [5, 5, 5, 5, 5], 25),
        Score(ScoreCategory.SIXES, [6, 6, 6, 6, 6], 30),
    ], True),
    # Bonus not achieved
    ([
        Score(ScoreCategory.ACES, [1, 2, 3, 4, 5], 1),
        Score(ScoreCategory.TWOS, [1, 2, 3, 4, 5], 2),
        Score(ScoreCategory.THREES, [1, 2, 3, 4, 5], 3),
        Score(ScoreCategory.FOURS, [1, 2, 3, 4, 5], 4),
        Score(ScoreCategory.FIVES, [1, 2, 3, 4, 5], 5),
        Score(ScoreCategory.SIXES, [1, 2, 3, 4, 5], 6),
    ], False),
    # Exactly 63 points
    ([
        Score(ScoreCategory.ACES, [1, 1, 1, 2, 3], 3),
        Score(ScoreCategory.TWOS, [2, 2, 2, 3, 4], 6),
        Score(ScoreCategory.THREES, [3, 3, 3, 4, 5], 9),
        Score(ScoreCategory.FOURS, [4, 4, 4, 5, 6], 12),
        Score(ScoreCategory.FIVES, [5, 5, 5, 6, 1], 15),
        Score(ScoreCategory.SIXES, [6, 6, 6, 1, 2], 18),
    ], True),
])
def test_upper_section_bonus(scores, expected_bonus):
    """Test upper section bonus calculation."""
    card = ScoreCard()
    for score in scores:
        card.assign_score(score)
    
    # Trigger bonus check by accessing total_score
    _ = card.total_score
    assert card.upper_section_bonus_awarded == expected_bonus


def test_upper_section_bonus_partial_scores():
    """Test upper section bonus with only some categories filled."""
    card = ScoreCard()
    
    # Fill only some upper section categories
    card.assign_score(Score(ScoreCategory.ACES, [1, 1, 1, 1, 1], 5))
    card.assign_score(Score(ScoreCategory.SIXES, [6, 6, 6, 6, 6], 30))
    
    _ = card.total_score
    assert card.upper_section_bonus_awarded is False


# Total Score Tests
def test_total_score_empty_card():
    """Test total score with no scores assigned."""
    card = ScoreCard()
    assert card.total_score == 0


def test_total_score_basic():
    """Test total score with basic scores."""
    card = ScoreCard()
    card.assign_score(Score(ScoreCategory.ACES, [1, 1, 1, 2, 3], 3))
    card.assign_score(Score(ScoreCategory.CHANCE, [1, 2, 3, 4, 5], 15))
    
    assert card.total_score == 18


def test_total_score_with_upper_bonus():
    """Test total score including upper section bonus."""
    card = ScoreCard()
    
    # Fill upper section to earn bonus
    upper_scores = [
        Score(ScoreCategory.ACES, [1, 1, 1, 1, 1], 5),
        Score(ScoreCategory.TWOS, [2, 2, 2, 2, 2], 10),
        Score(ScoreCategory.THREES, [3, 3, 3, 3, 3], 15),
        Score(ScoreCategory.FOURS, [4, 4, 4, 4, 4], 20),
        Score(ScoreCategory.FIVES, [5, 5, 5, 5, 5], 25),
        Score(ScoreCategory.SIXES, [6, 6, 6, 6, 6], 30),
    ]
    
    for score in upper_scores:
        card.assign_score(score)
    
    expected = sum(score.points for score in upper_scores) + 35  # 105 + 35 = 140
    assert card.total_score == expected


def test_total_score_with_yahtzee_bonus():
    """Test total score including Yahtzee bonus."""
    card = ScoreCard()
    
    # Assign original Yahtzee
    card.assign_score(Score(ScoreCategory.YAHTZEE, [5, 5, 5, 5, 5], 50))
    
    # Assign additional Yahtzee roll for bonus
    card.assign_score(Score(ScoreCategory.CHANCE, [6, 6, 6, 6, 6], 30))
    
    expected = 50 + 30 + 100  # Original scores + Yahtzee bonus
    assert card.total_score == expected


def test_total_score_with_all_bonuses():
    """Test total score with both upper section and Yahtzee bonuses."""
    card = ScoreCard()
    
    # Fill upper section to earn bonus
    upper_scores = [
        Score(ScoreCategory.ACES, [1, 1, 1, 1, 1], 5),
        Score(ScoreCategory.TWOS, [2, 2, 2, 2, 2], 10),
        Score(ScoreCategory.THREES, [3, 3, 3, 3, 3], 15),
        Score(ScoreCategory.FOURS, [4, 4, 4, 4, 4], 20),
        Score(ScoreCategory.FIVES, [5, 5, 5, 5, 5], 25),
        Score(ScoreCategory.SIXES, [6, 6, 6, 6, 6], 30),
    ]
    
    for score in upper_scores:
        card.assign_score(score)
    
    # Add Yahtzee and bonus
    card.assign_score(Score(ScoreCategory.YAHTZEE, [1, 1, 1, 1, 1], 50))
    card.assign_score(Score(ScoreCategory.CHANCE, [2, 2, 2, 2, 2], 10))
    
    base_score = sum(score.points for score in upper_scores) + 50 + 10  # 135
    expected = base_score + 35 + 100  # 135 + 35 + 100 = 270
    assert card.total_score == expected


# Repr Tests
def test_repr():
    """Test string representation of ScoreCard."""
    card = ScoreCard()
    repr_str = repr(card)
    assert isinstance(repr_str, str)
    assert "ScoreCard" in repr_str
    assert "scores=" in repr_str


def test_repr_with_scores():
    """Test string representation with some scores assigned."""
    card = ScoreCard()
    card.assign_score(Score(ScoreCategory.ACES, [1, 1, 1, 2, 3], 3))
    
    repr_str = repr(card)
    assert isinstance(repr_str, str)
    assert "ScoreCard" in repr_str


# Edge Cases
def test_multiple_calls_to_total_score():
    """Test that multiple calls to total_score give consistent results."""
    card = ScoreCard()
    card.assign_score(Score(ScoreCategory.ACES, [1, 1, 1, 2, 3], 3))
    
    score1 = card.total_score
    score2 = card.total_score
    assert score1 == score2


def test_bonus_persistence():
    """Test that bonuses persist after being awarded."""
    card = ScoreCard()
    
    # Fill upper section
    upper_scores = [
        Score(ScoreCategory.ACES, [1, 1, 1, 1, 1], 5),
        Score(ScoreCategory.TWOS, [2, 2, 2, 2, 2], 10),
        Score(ScoreCategory.THREES, [3, 3, 3, 3, 3], 15),
        Score(ScoreCategory.FOURS, [4, 4, 4, 4, 4], 20),
        Score(ScoreCategory.FIVES, [5, 5, 5, 5, 5], 25),
        Score(ScoreCategory.SIXES, [6, 6, 6, 6, 6], 30),
    ]
    
    for score in upper_scores:
        card.assign_score(score)
    
    # Check bonus is awarded
    _ = card.total_score
    assert card.upper_section_bonus_awarded is True
    
    # Add more scores and verify bonus is still there
    card.assign_score(Score(ScoreCategory.CHANCE, [1, 2, 3, 4, 5], 15))
    assert card.upper_section_bonus_awarded is True


def test_empty_roll_handling():
    """Test handling of empty rolls."""
    card = ScoreCard()
    score = Score(ScoreCategory.CHANCE, [], 0)
    card.assign_score(score)
    
    assert card.get_score(ScoreCategory.CHANCE) == score
    assert card.total_score == 0
