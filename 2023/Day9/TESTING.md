# Day 9 Testing

This directory contains comprehensive test cases for the Day 9 Advent of Code problem using pytest.

## Files

- `test_day_9.py`: Complete test suite with 22 test cases
- `requirements.txt`: Python dependencies for testing
- `day_9.py`: The solution being tested
- `example.txt`: Example input data from the problem description

## Running Tests

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Run all tests:

```bash
pytest test_day_9.py -v
```

### Run specific test categories:

```bash
# Test only the predict_recursive function
pytest test_day_9.py::TestPredictRecursive -v

# Test only the main function
pytest test_day_9.py::TestMainFunction -v

# Test only Part 2 examples
pytest test_day_9.py::TestPart2Examples -v

# Test only edge cases
pytest test_day_9.py::TestEdgeCases -v
```

## Test Coverage

The test suite includes:

### Core Examples from README

- All three example sequences from the problem description
- Verification that Part 1 sum equals 114
- Verification that Part 2 sum equals 2

### Function-level Testing

- `predict_recursive()` with various input types
- Edge cases like single elements, all zeros, constants
- Negative numbers and decreasing sequences

### Integration Testing

- Full `main()` function with example data
- Log output verification
- Empty data handling

### Part 2 Specific Tests

- Backwards extrapolation for all examples
- Verification of correct previous values (-3, 0, 5)

### Edge Cases

- Large numbers
- Quadratic sequences
- Different mathematical patterns
- File existence verification

## Expected Results

All 22 tests should pass, confirming that:

- Example sequence `[0, 3, 6, 9, 12, 15]` predicts `18`
- Example sequence `[1, 3, 6, 10, 15, 21]` predicts `28`
- Example sequence `[10, 13, 16, 21, 30, 45]` predicts `68`
- Part 1 total: 114
- Part 2 total: 2
