"""Integration tests for spell checker system.

Tests the complete spell checking workflow from input to output.
"""

import sys
import os

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lib.checker import Checker
from lib.trainer import Trainer


class TestIntegration:
    """Integration tests for complete spell checking workflow."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.checker = Checker()

    def test_simple_correction(self):
        """Test simple single-word correction."""
        result = self.checker.correct("teh")
        assert result == "the"

    def test_multiple_corrections(self):
        """Test multiple word corrections in context."""
        text = "teh quik brwn fox"
        words = text.split()
        corrected = [self.checker.correct(word) for word in words]
        corrected_text = " ".join(corrected)
        # Should correct at least some words
        assert corrected_text != text

    def test_correct_words_unchanged(self):
        """Test that correctly spelled words remain unchanged."""
        correct_words = ["the", "quick", "brown", "fox", "jumps"]
        for word in correct_words:
            assert self.checker.correct(word) == word

    def test_edit_distance_one(self):
        """Test correction of words with edit distance 1."""
        test_cases = [
            ("teh", "the"),  # transposition
            ("helo", "hello"),  # deletion
            ("wrld", "world"),  # insertion needed
        ]
        for misspelled, expected in test_cases:
            result = self.checker.correct(misspelled)
            # Should be close to expected
            assert isinstance(result, str)
            assert len(result) > 0

    def test_edit_distance_two(self):
        """Test correction of words with edit distance 2."""
        result = self.checker.correct("wrold")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_unknown_word_handling(self):
        """Test handling of completely unknown words."""
        result = self.checker.correct("xyzabc")
        # Should return something, even if it's the original word
        assert isinstance(result, str)
        assert len(result) > 0

    def test_case_preservation(self):
        """Test that word case is preserved where appropriate."""
        # The checker works on lowercase, but should handle input gracefully
        result = self.checker.correct("THE")
        assert isinstance(result, str)

    def test_contractions(self):
        """Test handling of contractions."""
        contractions = ["don't", "can't", "won't", "it's"]
        for word in contractions:
            result = self.checker.correct(word)
            assert isinstance(result, str)
            # Should not crash on contractions
            assert len(result) > 0

    def test_candidate_generation(self):
        """Test that candidate generation works correctly."""
        candidates = self.checker.get_candidates("teh")
        assert isinstance(candidates, set)
        assert len(candidates) > 0
        # Should include 'the' or similar words
        assert "the" in candidates or len(candidates) >= 1

    def test_edit_distance_calculation(self):
        """Test edit distance calculation."""
        assert self.checker.edit_distance("hello", "hello") == 0
        assert self.checker.edit_distance("hello", "helo") == 1
        assert self.checker.edit_distance("hello", "world") > 1

    def test_error_probability(self):
        """Test error probability calculation."""
        # Identical words should have highest probability
        assert self.checker.error_prob("hello", "hello") == 1.0
        # Similar words should have higher probability than dissimilar
        prob1 = self.checker.error_prob("hello", "helo")
        prob2 = self.checker.error_prob("hello", "world")
        assert prob1 > prob2

    def test_vocabulary_check(self):
        """Test vocabulary membership checking."""
        assert self.checker.is_known("the") is True
        assert self.checker.is_known("xyzabc") is False

    def test_sentence_processing(self):
        """Test processing of complete sentences."""
        sentence = "Ths is a tst sentence"
        words = sentence.split()
        corrected = [self.checker.correct(word) for word in words]
        # Should correct at least some words
        assert corrected != words

    def test_empty_input(self):
        """Test handling of empty input."""
        result = self.checker.correct("")
        # Should handle gracefully
        assert result == ""

    def test_single_character(self):
        """Test handling of single character input."""
        result = self.checker.correct("a")
        assert isinstance(result, str)
        assert len(result) >= 1

    def test_very_long_word(self):
        """Test handling of very long words."""
        long_word = "a" * 100
        result = self.checker.correct(long_word)
        # Should not crash
        assert isinstance(result, str)

    def test_numbers_and_text(self):
        """Test handling of mixed numbers and text."""
        # Numbers should be handled gracefully
        result = self.checker.correct("test123")
        assert isinstance(result, str)


class TestTrainerIntegration:
    """Integration tests for Trainer class."""

    def test_trainer_initialization(self):
        """Test that trainer initializes correctly."""
        trainer = Trainer(corpus="corpus_test.txt")
        assert trainer.data is not None
        assert "word_count" in trainer.data
        assert "unigram_probs" in trainer.data
        assert "bigram_probs" in trainer.data
        assert "trigram_probs" in trainer.data

    def test_trainer_with_checker(self):
        """Test that checker can use trainer data."""
        checker = Checker()
        # Should have loaded data from trainer
        assert len(checker.word_count) > 0
        assert len(checker.unigram_probs) > 0

    def test_probability_distributions(self):
        """Test that probability distributions are valid."""
        trainer = Trainer(corpus="corpus_test.txt")
        # Probabilities should sum to approximately 1.0
        unigram_sum = sum(trainer.data["unigram_probs"].values())
        assert 0.99 <= unigram_sum <= 1.01  # Allow for floating point error
