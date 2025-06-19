import pytest
from day_9 import predict_recursive, main
from io import StringIO
import sys


class TestPredictRecursive:
    """Test cases for the predict_recursive function."""

    def test_predict_recursive_example_1(self):
        """Test first example sequence: 0 3 6 9 12 15 -> 18"""
        sequence = [0, 3, 6, 9, 12, 15]
        expected = 18
        assert predict_recursive(sequence) == expected

    def test_predict_recursive_example_2(self):
        """Test second example sequence: 1 3 6 10 15 21 -> 28"""
        sequence = [1, 3, 6, 10, 15, 21]
        expected = 28
        assert predict_recursive(sequence) == expected

    def test_predict_recursive_example_3(self):
        """Test third example sequence: 10 13 16 21 30 45 -> 68"""
        sequence = [10, 13, 16, 21, 30, 45]
        expected = 68
        assert predict_recursive(sequence) == expected

    def test_predict_recursive_all_zeros(self):
        """Test sequence that's already all zeros."""
        sequence = [0, 0, 0, 0]
        expected = 0
        assert predict_recursive(sequence) == expected

    def test_predict_recursive_constant_sequence(self):
        """Test constant sequence: 5 5 5 5 -> 5"""
        sequence = [5, 5, 5, 5]
        expected = 5
        assert predict_recursive(sequence) == expected

    def test_predict_recursive_linear_sequence(self):
        """Test simple linear sequence: 1 2 3 4 -> 5"""
        sequence = [1, 2, 3, 4]
        expected = 5
        assert predict_recursive(sequence) == expected

    def test_predict_recursive_single_element(self):
        """Test single element sequence."""
        sequence = [42]
        expected = 42
        assert predict_recursive(sequence) == expected

    def test_predict_recursive_two_elements(self):
        """Test two element sequence: 1 3 -> 5"""
        sequence = [1, 3]
        expected = 5
        assert predict_recursive(sequence) == expected

    def test_predict_recursive_negative_numbers(self):
        """Test sequence with negative numbers: -3 -1 1 3 -> 5"""
        sequence = [-3, -1, 1, 3]
        expected = 5
        assert predict_recursive(sequence) == expected

    def test_predict_recursive_decreasing_sequence(self):
        """Test decreasing sequence: 10 8 6 4 -> 2"""
        sequence = [10, 8, 6, 4]
        expected = 2
        assert predict_recursive(sequence) == expected


class TestMainFunction:
    """Test cases for the main function with full example data."""

    def test_main_with_example_data(self, capsys):
        """Test main function with the complete example from README."""
        example_data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

        main(example_data)
        captured = capsys.readouterr()

        # Check that Part 1 sum is 114 (18 + 28 + 68)
        assert "Part 1: 114" in captured.out
        # Check that Part 2 sum is 2 (-3 + 0 + 5)
        assert "Part 2: 2" in captured.out

    def test_main_with_single_line(self, capsys):
        """Test main function with single line input."""
        single_line_data = "0 3 6 9 12 15"

        main(single_line_data)
        captured = capsys.readouterr()

        # Part 1: should predict 18
        assert "Part 1: 18" in captured.out
        # Part 2: should predict -3 (reverse of [0,3,6,9,12,15] is [15,12,9,6,3,0])
        assert "Part 2: -3" in captured.out

    def test_main_with_log_enabled(self, capsys):
        """Test main function with logging enabled."""
        example_data = "1 2 3 4"

        main(example_data, log=True)
        captured = capsys.readouterr()

        # Check that debug information is printed
        assert "Part 1:" in captured.out
        assert "Lines:" in captured.out
        assert "Predictions:" in captured.out
        assert "Part 2:" in captured.out

    def test_main_empty_data(self, capsys):
        """Test main function with empty data."""
        empty_data = ""

        main(empty_data)
        captured = capsys.readouterr()

        # Should handle empty input gracefully
        assert "Part 1: 0" in captured.out
        assert "Part 2: 0" in captured.out


class TestPart2Examples:
    """Test cases specifically for Part 2 (backwards extrapolation)."""

    def test_part2_example_1_backwards(self):
        """Test first example backwards: [15,12,9,6,3,0] should predict -3"""
        # Reverse of [0,3,6,9,12,15] is [15,12,9,6,3,0]
        reversed_sequence = [15, 12, 9, 6, 3, 0]
        expected = -3
        assert predict_recursive(reversed_sequence) == expected

    def test_part2_example_2_backwards(self):
        """Test second example backwards: [21,15,10,6,3,1] should predict 0"""
        # Reverse of [1,3,6,10,15,21] is [21,15,10,6,3,1]
        reversed_sequence = [21, 15, 10, 6, 3, 1]
        expected = 0
        assert predict_recursive(reversed_sequence) == expected

    def test_part2_example_3_backwards(self):
        """Test third example backwards: [45,30,21,16,13,10] should predict 5"""
        # Reverse of [10,13,16,21,30,45] is [45,30,21,16,13,10]
        reversed_sequence = [45, 30, 21, 16, 13, 10]
        expected = 5
        assert predict_recursive(reversed_sequence) == expected


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_large_numbers(self):
        """Test with large numbers."""
        sequence = [1000000, 1000001, 1000002, 1000003]
        expected = 1000004
        assert predict_recursive(sequence) == expected

    def test_quadratic_sequence(self):
        """Test quadratic sequence: 1 4 9 16 (squares) -> 25"""
        sequence = [1, 4, 9, 16]
        expected = 25
        assert predict_recursive(sequence) == expected

    def test_fibonacci_like_sequence(self):
        """Test Fibonacci-like sequence: 1 1 2 3 5 -> 11 (using difference algorithm)"""
        sequence = [1, 1, 2, 3, 5]
        expected = 11  # Algorithm uses differences, not Fibonacci logic
        assert predict_recursive(sequence) == expected

    def test_alternating_differences(self):
        """Test sequence with alternating differences."""
        sequence = [0, 1, 1, 4, 8]  # differences: 1, 0, 3, 4
        result = predict_recursive(sequence)
        # This should work according to the algorithm
        assert isinstance(result, int)


# Test fixtures and utilities
@pytest.fixture
def example_file_content():
    """Fixture providing the example file content."""
    return """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def test_example_file_exists():
    """Test that the example file exists and contains expected data."""
    try:
        with open("/Users/tomfuller/advent/2023/Day9/example.txt", "r") as f:
            content = f.read().strip()

        lines = content.split("\n")
        assert len(lines) == 3
        assert lines[0] == "0 3 6 9 12 15"
        assert lines[1] == "1 3 6 10 15 21"
        assert lines[2] == "10 13 16 21 30 45"
    except FileNotFoundError:
        pytest.skip("Example file not found")


if __name__ == "__main__":
    pytest.main([__file__])
