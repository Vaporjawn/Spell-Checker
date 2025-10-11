import re
from .trainer import Trainer


class Checker:
    def __init__(self, trainer=Trainer):
        trainer = trainer()
        data = trainer.data
        self.word_count = data["word_count"]
        self.unigram_probs = data["unigram_probs"]
        self.bigram_probs = data["bigram_probs"]
        self.trigram_probs = data["trigram_probs"]

    def knowns(self, words):
        return set(w for w in words if w in self.word_count)

    def is_known(self, word):
        return word in self.word_count

    def words(self, text):
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

    def edit_distance(self, s1, s2):
        """Calculate the Levenshtein distance between two strings."""
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

    def error_prob(self, error, poss):
        dist = self.edit_distance(error, poss)
        prob = (1 / (2**dist)) if dist > 0 else 1.0
        return prob

    def correct(self, word):
        """Return the most likely correct spelling of word."""
        # If the word is already known, return it as is
        if self.is_known(word):
            return word

        # Generate candidates and find the best correction
        candidates = self.get_candidates(word)
        return max(candidates, key=lambda x: self.word_count[x])

    def get_candidates(self, word):
        """Generate possible corrections for word."""
        # First, try known words
        known_candidates = self.knowns([word])
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

    def edits1(self, word):
        """Generate all strings one edit away from word."""
        letters = "abcdefghijklmnopqrstuvwxyz"
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)
