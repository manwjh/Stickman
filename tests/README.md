# Testing

## Run Tests

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest

# Run with coverage report
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_skeleton.py

# Run specific test
pytest tests/test_skeleton.py::TestSkeleton::test_create_standard_skeleton
```

## Test Structure

```
tests/
├── test_skeleton.py      # Skeleton system tests
├── test_llm_service.py   # LLM integration tests
├── test_validator.py     # Validation logic tests
└── test_integration.py   # End-to-end tests
```

## Coverage Requirements

- Minimum coverage: 80%
- Target coverage: >85%
- Critical paths must have 100% coverage

## Writing Tests

### Example Test

```python
def test_create_skeleton():
    """Test creating a standard skeleton"""
    skeleton = Skeleton.create_standard("test", 120)
    assert skeleton.base_height == 120
    assert len(skeleton.bones) == 11
```

### Using Fixtures

```python
@pytest.fixture
def standard_skeleton():
    return Skeleton.create_standard("test", 120)

def test_with_fixture(standard_skeleton):
    assert standard_skeleton.character_id == "test"
```

## Continuous Integration

Tests run automatically on:
- Every commit
- Pull requests
- Before deployment

## Performance Tests

See `tests/test_performance.py` for:
- Load testing
- Latency benchmarks
- Memory usage tests
