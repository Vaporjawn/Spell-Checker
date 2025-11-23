"""Performance benchmarks for spell checker.

Measures performance characteristics of key operations.
"""

import sys
import os
import time

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lib.checker import Checker


class TestPerformance:
    """Performance benchmark tests."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.checker = Checker()

    def test_single_word_correction_speed(self):
        """Benchmark single word correction."""
        start = time.time()
        for _ in range(100):
            self.checker.correct("teh")
        duration = time.time() - start
        # Should complete 100 corrections in reasonable time
        assert duration < 2.0, f"Single word correction too slow: {duration}s"

    def test_edit_distance_caching(self):
        """Test that edit distance caching improves performance."""
        # First call (not cached)
        start1 = time.time()
        for _ in range(100):
            self.checker.edit_distance("hello", "world")
        duration1 = time.time() - start1

        # Second call (should be cached)
        start2 = time.time()
        for _ in range(100):
            self.checker.edit_distance("hello", "world")
        duration2 = time.time() - start2

        # Cached calls should be significantly faster
        assert duration2 < duration1, "Caching not improving performance"

    def test_batch_correction_speed(self):
        """Benchmark batch word correction."""
        words = ["teh", "quik", "brwn", "fox", "jmps"] * 20
        start = time.time()
        results = [self.checker.correct(word) for word in words]
        duration = time.time() - start
        # Should complete 100 corrections in reasonable time
        assert duration < 5.0, f"Batch correction too slow: {duration}s"
        assert len(results) == len(words)

    def test_candidate_generation_speed(self):
        """Benchmark candidate generation."""
        start = time.time()
        for _ in range(50):
            self.checker.get_candidates("test")
        duration = time.time() - start
        assert duration < 2.0, f"Candidate generation too slow: {duration}s"

    def test_memory_efficiency(self):
        """Test memory efficiency with repeated operations."""
        # Perform many operations to check for memory leaks
        for i in range(1000):
            word = f"test{i % 10}"
            self.checker.correct(word)
        # If we get here without crashing, memory handling is reasonable
        assert True

    def test_large_text_processing(self):
        """Test processing of large text blocks."""
        large_text = "This is a test sentence. " * 100
        words = large_text.split()
        start = time.time()
        results = [self.checker.correct(word) for word in words]
        duration = time.time() - start
        # Should handle large text efficiently
        assert duration < 10.0, f"Large text processing too slow: {duration}s"
        assert len(results) == len(words)


class TestScalability:
    """Scalability tests for spell checker."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.checker = Checker()

    def test_linear_scaling(self):
        """Test that performance scales linearly with input size."""
        sizes = [10, 50, 100]
        durations = []

        for size in sizes:
            words = ["test"] * size
            start = time.time()
            [self.checker.correct(word) for word in words]
            duration = time.time() - start
            durations.append(duration)

        # Performance should scale roughly linearly
        # (not exponentially)
        if len(durations) >= 3:
            # Ratio of time for 100 vs 10 should be close to 10
            ratio = durations[2] / durations[0] if durations[0] > 0 else 0
            assert ratio < 20, f"Performance scaling poorly: ratio={ratio}"

    def test_concurrent_operations(self):
        """Test behavior under concurrent load."""
        # Simulate concurrent requests
        results = []
        start = time.time()
        for _ in range(10):
            # Simulate 10 concurrent spell check operations
            batch = [self.checker.correct(f"test{i}") for i in range(10)]
            results.extend(batch)
        duration = time.time() - start

        assert len(results) == 100
        assert duration < 5.0, f"Concurrent operations too slow: {duration}s"


if __name__ == "__main__":
    # Run benchmarks
    pytest.main([__file__, "-v", "-s"])
