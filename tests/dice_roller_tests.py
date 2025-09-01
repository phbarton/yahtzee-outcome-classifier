from src.dice_roller import DiceRoller


# Initialization Tests
def test_default_initialization():
    """Test default initialization parameters."""
    roller = DiceRoller()
    assert roller.num_dice == 5
    assert roller.die_size == 6
    assert roller.rng is not None

def test_custom_num_dice():
    """Test initialization with custom number of dice."""
    roller = DiceRoller(num_dice=3)
    assert roller.num_dice == 3
    assert roller.die_size == 6

def test_custom_die_size():
    """Test initialization with custom die size."""
    roller = DiceRoller(die_size=8)
    assert roller.num_dice == 5
    assert roller.die_size == 8

def test_custom_seed():
    """Test initialization with custom seed."""
    roller = DiceRoller(seed=42)
    assert roller.num_dice == 5
    assert roller.die_size == 6
    assert roller.rng is not None

def test_all_custom_parameters():
    """Test initialization with all custom parameters."""
    roller = DiceRoller(num_dice=4, die_size=10, seed=123)
    assert roller.num_dice == 4
    assert roller.die_size == 10
    assert roller.rng is not None


# Roll Tests
def test_roll_returns_correct_number_of_dice():
    """Test that roll returns the correct number of dice."""
    roller = DiceRoller(num_dice=5)
    result = roller.roll()
    assert len(result) == 5

def test_roll_returns_sorted_list():
    """Test that roll returns a sorted list."""
    roller = DiceRoller(seed=42)
    result = roller.roll()
    assert result == sorted(result)

def test_roll_values_within_range():
    """Test that all rolled values are within the expected range."""
    roller = DiceRoller(seed=42)
    result = roller.roll()
    for value in result:
        assert 1 <= value <= 6

def test_roll_with_custom_die_size():
    """Test rolling with custom die size."""
    roller = DiceRoller(die_size=8, seed=42)
    result = roller.roll()
    for value in result:
        assert 1 <= value <= 8

def test_roll_with_custom_num_dice():
    """Test rolling with custom number of dice."""
    roller = DiceRoller(num_dice=3, seed=42)
    result = roller.roll()
    assert len(result) == 3
    for value in result:
        assert 1 <= value <= 6

def test_roll_deterministic_with_seed():
    """Test that rolling with the same seed produces consistent results."""
    roller1 = DiceRoller(seed=42)
    roller2 = DiceRoller(seed=42)
    
    result1 = roller1.roll()
    result2 = roller2.roll()
    
    assert result1 == result2

def test_roll_different_results_without_seed():
    """Test that rolling without seed produces different results (probabilistically)."""
    roller = DiceRoller()
    results = [roller.roll() for _ in range(10)]
    
    # It's extremely unlikely that all 10 rolls are identical
    assert len(set(tuple(r) for r in results)) > 1


# Reroll Tests
def test_reroll_single_die():
    """Test rerolling a single die."""
    roller = DiceRoller(seed=42)
    initial_dice = [1, 2, 3, 4, 5]
    result = roller.reroll(initial_dice, [0])
    
    # The result should be sorted and have the same length
    assert len(result) == 5
    assert result == sorted(result)
    
    # Only the first die should have changed (with high probability)
    # Since we're using a seed, we can test the exact expected result
    expected_reroll_value = DiceRoller(seed=42)._roll_dice(1)[0]
    expected_result = sorted([expected_reroll_value, 2, 3, 4, 5])
    assert result == expected_result

def test_reroll_multiple_dice():
    """Test rerolling multiple dice."""
    roller = DiceRoller(seed=42)
    initial_dice = [1, 2, 3, 4, 5]
    result = roller.reroll(initial_dice, [0, 2, 4])
    
    assert len(result) == 5
    assert result == sorted(result)
    
    # All values should be valid dice values
    for value in result:
        assert 1 <= value <= 6

def test_reroll_no_dice():
    """Test rerolling with empty indices list."""
    roller = DiceRoller()
    initial_dice = [1, 2, 3, 4, 5]
    result = roller.reroll(initial_dice, [])
    
    # Should return the same dice (sorted)
    assert result == sorted(initial_dice)

def test_reroll_all_dice():
    """Test rerolling all dice."""
    roller = DiceRoller(seed=42)
    initial_dice = [1, 2, 3, 4, 5]
    result = roller.reroll(initial_dice, [0, 1, 2, 3, 4])
    
    assert len(result) == 5
    assert result == sorted(result)
    for value in result:
        assert 1 <= value <= 6

def test_reroll_invalid_indices_ignored():
    """Test that invalid indices are ignored during reroll."""
    roller = DiceRoller(seed=42)
    initial_dice = [1, 2, 3, 4, 5]
    
    # Include some invalid indices
    result = roller.reroll(initial_dice, [0, 2, 10, -1, 7])
    
    assert len(result) == 5
    assert result == sorted(result)
    
    # All values should still be valid
    for value in result:
        assert 1 <= value <= 6

def test_reroll_preserves_original_list():
    """Test that reroll doesn't modify the original dice list."""
    roller = DiceRoller()
    initial_dice = [1, 2, 3, 4, 5]
    original_dice = initial_dice.copy()
    
    roller.reroll(initial_dice, [0, 2])
    
    # Original list should be unchanged
    assert initial_dice == original_dice

def test_reroll_deterministic_with_seed():
    """Test that rerolling with the same seed produces consistent results."""
    initial_dice = [1, 2, 3, 4, 5]
    
    roller1 = DiceRoller(seed=42)
    roller2 = DiceRoller(seed=42)
    
    result1 = roller1.reroll(initial_dice, [0, 2])
    result2 = roller2.reroll(initial_dice, [0, 2])
    
    assert result1 == result2


# Private Method Tests
def test_roll_dice_single_die():
    """Test _roll_dice with single die."""
    roller = DiceRoller(seed=42)
    result = roller._roll_dice(1)
    
    assert len(result) == 1
    assert 1 <= result[0] <= 6

def test_roll_dice_multiple_dice():
    """Test _roll_dice with multiple dice."""
    roller = DiceRoller(seed=42)
    result = roller._roll_dice(3)
    
    assert len(result) == 3
    for value in result:
        assert 1 <= value <= 6

def test_roll_dice_zero_dice():
    """Test _roll_dice with zero dice."""
    roller = DiceRoller()
    result = roller._roll_dice(0)
    
    assert len(result) == 0
    assert result == []

def test_roll_dice_with_custom_die_size():
    """Test _roll_dice respects custom die size."""
    roller = DiceRoller(die_size=10, seed=42)
    result = roller._roll_dice(5)
    
    for value in result:
        assert 1 <= value <= 10


# Edge Case Tests
def test_single_die_roller():
    """Test roller with only one die."""
    roller = DiceRoller(num_dice=1, seed=42)
    result = roller.roll()
    
    assert len(result) == 1
    assert 1 <= result[0] <= 6

def test_large_number_of_dice():
    """Test roller with large number of dice."""
    roller = DiceRoller(num_dice=100, seed=42)
    result = roller.roll()
    
    assert len(result) == 100
    assert result == sorted(result)
    for value in result:
        assert 1 <= value <= 6

def test_custom_die_size_edge_cases():
    """Test with different die sizes."""
    # Test with 2-sided die (coin flip)
    roller = DiceRoller(die_size=2, seed=42)
    result = roller.roll()
    for value in result:
        assert 1 <= value <= 2
    
    # Test with 20-sided die
    roller = DiceRoller(die_size=20, seed=42)
    result = roller.roll()
    for value in result:
        assert 1 <= value <= 20

def test_reroll_with_duplicate_indices():
    """Test rerolling with duplicate indices."""
    roller = DiceRoller(seed=42)
    initial_dice = [1, 2, 3, 4, 5]
    
    # Should handle duplicate indices gracefully
    result = roller.reroll(initial_dice, [0, 0, 2, 2])
    
    assert len(result) == 5
    assert result == sorted(result)
    for value in result:
        assert 1 <= value <= 6


# Randomness Tests
def test_roll_distribution_approximately_uniform():
    """Test that rolls are approximately uniformly distributed."""
    roller = DiceRoller(num_dice=1)
    
    # Roll many times and check distribution
    num_rolls = 6000
    results = []
    for _ in range(num_rolls):
        results.extend(roller.roll())
    
    # Count occurrences of each value
    counts = {i: results.count(i) for i in range(1, 7)}
    
    # Each value should appear roughly 1000 times (±200 for some tolerance)
    expected_count = num_rolls // 6
    tolerance = expected_count * 0.2  # 20% tolerance
    
    for value, count in counts.items():
        assert abs(count - expected_count) < tolerance, f"Value {value} appeared {count} times, expected ~{expected_count}"

def test_different_seeds_produce_different_results():
    """Test that different seeds produce different results."""
    roller1 = DiceRoller(seed=42)
    roller2 = DiceRoller(seed=123)
    
    results1 = [roller1.roll() for _ in range(10)]
    results2 = [roller2.roll() for _ in range(10)]
    
    # Should be very unlikely that all results are identical
    assert results1 != results2

def test_same_seed_reproducible_sequence():
    """Test that the same seed produces reproducible sequences."""
    roller1 = DiceRoller(seed=42)
    roller2 = DiceRoller(seed=42)
    
    # Generate several rolls and rerolls
    results1 = []
    results2 = []
    
    for _ in range(5):
        roll1 = roller1.roll()
        roll2 = roller2.roll()
        results1.append(roll1)
        results2.append(roll2)
        
        # Also test rerolls
        reroll1 = roller1.reroll(roll1, [0, 2])
        reroll2 = roller2.reroll(roll2, [0, 2])
        results1.append(reroll1)
        results2.append(reroll2)
    
    assert results1 == results2


# Integration Tests
def test_yahtzee_game_simulation():
    """Test a simplified Yahtzee turn simulation."""
    roller = DiceRoller(seed=42)
    
    # Initial roll
    first_roll = roller.roll()
    assert len(first_roll) == 5
    
    # First reroll (keep some dice)
    second_roll = roller.reroll(first_roll, [0, 2, 4])
    assert len(second_roll) == 5
    
    # Second reroll (keep different dice)
    third_roll = roller.reroll(second_roll, [1, 3])
    assert len(third_roll) == 5
    
    # All results should be valid
    for roll in [first_roll, second_roll, third_roll]:
        assert all(1 <= value <= 6 for value in roll)
        assert roll == sorted(roll)

def test_multiple_rollers_independence():
    """Test that multiple roller instances work independently."""
    roller1 = DiceRoller(seed=42)
    roller2 = DiceRoller(seed=123)
    
    # Interleave operations
    result1a = roller1.roll()
    result2a = roller2.roll()
    result1b = roller1.reroll(result1a, [0, 1])
    result2b = roller2.reroll(result2a, [2, 3, 4])
    
    # Results should be different due to different seeds
    assert result1a != result2a
    assert result1b != result2b
    
    # But each roller should maintain its own state
    roller1_copy = DiceRoller(seed=42)
    roller2_copy = DiceRoller(seed=123)
    
    copy_result1a = roller1_copy.roll()
    copy_result2a = roller2_copy.roll()
    
    assert result1a == copy_result1a
    assert result2a == copy_result2a


# Error Handling Tests
def test_reroll_with_empty_dice_list():
    """Test rerolling with an empty dice list."""
    roller = DiceRoller()
    result = roller.reroll([], [])
    assert result == []

def test_reroll_preserves_dice_not_in_indices():
    """Test that dice not specified in indices remain unchanged."""
    roller = DiceRoller(seed=42)
    initial_dice = [1, 2, 3, 4, 5]
    
    # Only reroll index 2
    result = roller.reroll(initial_dice, [2])
    
    # Check that the result is valid and sorted
    assert len(result) == 5
    assert result == sorted(result)
    for value in result:
        assert 1 <= value <= 6

def test_reroll_negative_indices_ignored():
    """Test that negative indices are properly ignored."""
    roller = DiceRoller(seed=42)
    initial_dice = [1, 2, 3, 4, 5]
    
    # Should only reroll index 1, ignore negative indices
    result = roller.reroll(initial_dice, [-1, 1, -5])
    
    assert len(result) == 5
    assert result == sorted(result)

def test_reroll_out_of_bounds_indices_ignored():
    """Test that out-of-bounds indices are properly ignored."""
    roller = DiceRoller(seed=42)
    initial_dice = [1, 2, 3, 4, 5]
    
    # Should only reroll valid indices, ignore out-of-bounds
    result = roller.reroll(initial_dice, [1, 5, 10, 100])
    
    assert len(result) == 5
    assert result == sorted(result)


# Statistical Tests
def test_roll_produces_all_possible_values():
    """Test that rolling many times produces all possible die values."""
    roller = DiceRoller(num_dice=1)
    
    # Roll many times to get all possible values
    all_results = []
    for _ in range(1000):
        all_results.extend(roller.roll())
    
    unique_values = set(all_results)
    expected_values = set(range(1, 7))
    
    assert unique_values == expected_values

def test_reroll_maintains_die_constraints():
    """Test that rerolled dice maintain proper constraints."""
    roller = DiceRoller(die_size=8, seed=42)
    
    # Test multiple rerolls
    dice = [1, 2, 3, 4, 5]
    for _ in range(10):
        dice = roller.reroll(dice, [0, 1, 2, 3, 4])
        assert len(dice) == 5
        assert dice == sorted(dice)
        for value in dice:
            assert 1 <= value <= 8
