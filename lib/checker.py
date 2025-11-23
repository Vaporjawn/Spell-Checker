"""Spell checker module with contextual correction.

Provides spell checking functionality using n-gram language models
and edit distance algorithms for word correction.
"""

import re
from functools import lru_cache
from typing import Set, List, Dict

from .trainer import Trainer


class Checker:
    """Spell checker using n-gram language models and edit distance.

    Attributes:
        word_count: Dictionary of word frequencies
        unigram_probs: Unigram probability distribution
        bigram_probs: Bigram probability distribution
        trigram_probs: Trigram probability distribution
    """

    def __init__(self, trainer: type = Trainer) -> None:
        """Initialize the spell checker with trained model data.

        Args:
            trainer: Trainer class to use for loading language model data
        """
        trainer_instance = trainer()
        data = trainer_instance.data
        self.word_count: Dict = data["word_count"]
        self.unigram_probs: Dict = data["unigram_probs"]
        self.bigram_probs: Dict = data["bigram_probs"]
        self.trigram_probs: Dict = data["trigram_probs"]

    def knowns(self, words: Set[str]) -> Set[str]:
        """Return subset of words that exist in the vocabulary.

        Args:
            words: Set of words to check

        Returns:
            Set of known words from the vocabulary
        """
        return set(w for w in words if w in self.word_count)

    def is_known(self, word: str) -> bool:
        """Check if a word exists in the vocabulary.

        Args:
            word: Word to check

        Returns:
            True if word is in vocabulary, False otherwise
        """
        return word in self.word_count

    def words(self, text: str) -> List[str]:
        """Extract words from text using regex.

        Args:
            text: Input text to tokenize

        Returns:
            List of lowercase words and contractions
        """
        return re.findall("[a-z']+", text.lower())

    def check_sentence(self, sentence):
        sentence_list = ["^"] + self.words(sentence) + ["$"]
        corrections_list = []
        for i, word in enumerate(sentence_list):
            if self.is_known(word) or word in ["^", "$"]:
                continue
            else:
                before = sentence_list[i - 1]
                after = sentence_list[i + 1]
                corrections_list.append(self.calculate(word, before, after))
        return corrections_list

    def calculate(self, word, before, after):
        rl = []
        for poss in self.word_count:
            prob = self.prob(word, poss, before, after)
            rl.append((poss, prob))
        rl.sort(key=lambda tup: tup[1])
        rl.reverse()
        return rl[:5]

    def prob(self, word, poss, before, after):
        a, b, c, d, e = 1, 1, 1, 1, 1
        r = (
            (a * self.unigram_prob(poss))
            + (b * self.bigram_prob((poss, after)))
            + (c * self.bigram_prob((before, poss)))
            + (d * self.trigram_prob((before, poss, after)))
            + (e * self.error_prob(word, poss))
        )
        return r

    def unigram_prob(self, word):
        prob = self.unigram_probs[word]
        return prob

    def bigram_prob(self, bigram):
        prob = self.bigram_probs[bigram]
        return prob

    def trigram_prob(self, trigram):
        prob = self.trigram_probs[trigram]
        return prob

    @lru_cache(maxsize=1024)
    def edit_distance(self, s1: str, s2: str) -> int:
        """Calculate the Levenshtein distance between two strings.

        Uses dynamic programming to compute minimum edit distance.
        Results are cached for performance.

        Args:
            s1: First string
            s2: Second string

        Returns:
            Minimum number of single-character edits (insertions,
            deletions, or substitutions) required to change s1 into s2
        """
        if len(s1) < len(s2):
            return self.edit_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def error_prob(self, error: str, poss: str) -> float:
        """Calculate probability of error transformation.

        Uses inverse exponential of edit distance to model
        the likelihood of one word being mistyped as another.

        Args:
            error: The misspelled word
            poss: A possible correct word

        Returns:
            Probability value between 0 and 1, where higher values
            indicate more likely corrections
        """
        dist = self.edit_distance(error, poss)
        prob = (1 / (2**dist)) if dist > 0 else 1.0
        return prob

    def correct(self, word: str) -> str:
        """Return the most likely correct spelling of word.

        Uses a cascading approach:
        1. If word is known, return as-is
        2. Try edit distance 1 candidates
        3. Try edit distance 2 candidates
        4. If no candidates found, return original word

        Args:
            word: Word to correct

        Returns:
            Most likely correct spelling based on word frequency
        """
        # Handle empty strings
        if not word or not word.strip():
            return ""

        # If the word is already known, return it as is
        if self.is_known(word):
            return word

        # Generate candidates and find the best correction
        candidates = self.get_candidates(word)
        return max(candidates, key=lambda x: self.word_count[x])

    def get_candidates(self, word: str) -> Set[str]:
        """Generate possible corrections for word.

        Tries progressively more distant edits until candidates are found.

        Args:
            word: Word to generate candidates for

        Returns:
            Set of candidate corrections
        """
        # First, try known words
        known_candidates = self.knowns({word})
        if known_candidates:
            return known_candidates

        # Try edit distance 1
        edit1 = self.edits1(word)
        known_edit1 = self.knowns(edit1)
        if known_edit1:
            return known_edit1

        # Try edit distance 2
        edit2 = {e2 for e1 in edit1 for e2 in self.edits1(e1)}
        known_edit2 = self.knowns(edit2)
        if known_edit2:
            return known_edit2

        # If nothing found, return the original word
        return {word}

    def edits1(self, word: str) -> Set[str]:
        """Generate all strings one edit away from word.

        Generates all possible single-edit variations including:
        - Deletions: Removing one character
        - Transpositions: Swapping adjacent characters
        - Replacements: Changing one character
        - Insertions: Adding one character

        Args:
            word: Input word to generate edits for

        Returns:
            Set of all possible single-edit variations
        """
        letters = "abcdefghijklmnopqrstuvwxyz"
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)
