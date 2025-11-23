"""Language model trainer for spell checker.

Trains n-gram language models from a text corpus for use
in contextual spell checking and correction.
"""

import collections
import os
import re
from typing import List, Tuple, Dict, DefaultDict


class Trainer:
    """Train n-gram language models from text corpus.

    Attributes:
        corpus: Raw text corpus string
        data: Dictionary containing trained models and probabilities
    """

    def __init__(self, corpus: str = "corpus.txt") -> None:
        """Initialize and train language models from corpus.

        Args:
            corpus: Filename of the corpus file in data/ directory

        Raises:
            FileNotFoundError: If corpus file doesn't exist
            IOError: If corpus file cannot be read
        """
        corpus_path = os.path.join("data", corpus)
        try:
            with open(corpus_path, "r", encoding="utf-8") as f:
                self.corpus = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Corpus file not found: {corpus_path}. "
                "Please ensure the data directory and corpus file exist."
            )
        except IOError as e:
            raise IOError(f"Error reading corpus file {corpus_path}: {str(e)}")

        self.data: Dict = {}
        word_list = self.words(self.corpus)
        bigram_list = self.bigrams(self.corpus)
        trigram_list = self.trigrams(self.corpus)
        word_count = self.train_model(word_list)
        bigram_count = self.train_model(bigram_list)
        trigram_count = self.train_model(trigram_list)
        self.data["word_count"] = word_count
        self.data["bigram_count"] = bigram_count
        self.data["trigram_count"] = trigram_count
        self.data["unigram_probs"] = self.get_probs(word_count)
        self.data["bigram_probs"] = self.get_probs(bigram_count)
        self.data["trigram_probs"] = self.get_probs(trigram_count)

    def get_probs(self, count: DefaultDict) -> DefaultDict:
        """Calculate probability distribution from frequency counts.

        Args:
            count: Dictionary of n-gram frequency counts

        Returns:
            Dictionary mapping n-grams to their probability values
        """
        prob_dict = collections.defaultdict(lambda: 0)
        denom = sum(count.values())
        for gram in count:
            prob_dict[gram] = count[gram] / denom
        return prob_dict

    def words(self, text: str) -> List[str]:
        """Extract words from text using regex.

        Args:
            text: Input text to tokenize

        Returns:
            List of lowercase words and contractions
        """
        return re.findall("[a-z']+", text.lower())

    def bigrams(self, text: str) -> List[Tuple[str, str]]:
        """Extract bigrams (word pairs) from text.

        Args:
            text: Input text to process

        Returns:
            List of bigram tuples with sentence boundary markers (^, $)
        """
        word_list = []
        lines = filter(None, re.split(r"[.?!\n]+", text))
        for line in lines:
            mod_line = ["^"] + self.words(line) + ["$"]
            for i in range(len(mod_line) - 1):
                word_list.append((mod_line[i], mod_line[i + 1]))
        return word_list

    def trigrams(self, text: str) -> List[Tuple[str, str, str]]:
        """Extract trigrams (word triples) from text.

        Args:
            text: Input text to process

        Returns:
            List of trigram tuples with sentence boundary markers (^, $)
        """
        word_list = []
        lines = filter(None, re.split(r"[.?!\n]+", text))
        for line in lines:
            mod_line = ["^"] + self.words(line) + ["$"]
            for i in range(len(mod_line) - 2):
                word_list.append((mod_line[i], mod_line[i + 1], mod_line[i + 2]))
        return word_list

    def train_model(self, features: List) -> DefaultDict:
        """Train frequency model from feature list.

        Uses add-one (Laplace) smoothing by initializing all
        counts to 1 before counting occurrences.

        Args:
            features: List of features (words or n-grams) to count

        Returns:
            DefaultDict mapping features to their frequency counts
        """
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model
