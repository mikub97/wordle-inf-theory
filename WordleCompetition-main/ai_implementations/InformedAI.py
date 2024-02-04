import numpy as np
import pandas as pd
import itertools
import math
from WordleAI import WordleAI,LetterInformation
from WordleJudge import WordleJudge

class InformedAI(WordleAI):

    # UNKOWN = auto()  # light grey in the game
    # PRESENT = auto()  # yellow in the game
    # NOT_PRESENT = auto()  # dark grey in the game
    # CORRECT = auto()  # green in the game
    def __init__(self, words):
        super().__init__(words)
        self.judge = WordleJudge(words)
        self._name_of_mine= "InformedPlayer"
        self.possible_feedback_permutations = list(itertools.product([
            LetterInformation.CORRECT,
            LetterInformation.NOT_PRESENT,
            LetterInformation.PRESENT
        ], repeat=5))


    def calc_word_distribution(self, word: str):
        result = []
        total = 0
        for feedback in self.possible_feedback_permutations:
            numb = len(self.narrow_guesses((word, feedback)))
            result.append(numb)
            total += numb
        return np.array(result) / total

    def calc_entropy(self, dists):
        vals = dists[dists > 0]
        return -np.sum(vals * np.log2(vals))

    def calc_distribution_and_entropy(self, word):
        dist = self.calc_word_distribution(word)
        return ({
            'word': word,
            'distribution': dist,
            'entropy': self.calc_entropy(dist)
        })

    def calc_distributions_and_entropies(self, words):
        result = []
        for i, w in enumerate(words):
            result.append(self.calc_distribution_and_entropy(w))
        return result

    def narrow_guesses(self, guess):
        if not isinstance(guess, tuple):
            raise Exception(f"Wrong type for 'guess' argument. Should be tuple,   got {type(guess)}")
        possibilities = self.actual_possibilities
        for i, (letter, state) in enumerate(zip(list(guess[0].upper()), guess[1])):
            if state == LetterInformation.NOT_PRESENT:
                possibilities = tuple(word for word in possibilities if letter not in word)
            if state == LetterInformation.CORRECT:
                possibilities = tuple(word for word in possibilities if word[i] == letter)
            if state == LetterInformation.PRESENT:
                possibilities = tuple(word for word in possibilities if (letter in word and word[i] != letter))
        return possibilities


    def guess(self, guess_history):

        if len(guess_history) == 0:
            self.current_distribution = pd.read_csv("../data/word_distributions.csv",
                                                    usecols=["word", "distribution", "entropy"]) \
                .sort_values(by="entropy", ascending=False)
            self.actual_possibilities = list(self.current_distribution[:]['word'])
            return self.current_distribution.iloc[0]['word'].lower()
        self.actual_possibilities = self.narrow_guesses(guess_history[-1])
        self.current_distribution = pd.DataFrame(
            self.calc_distributions_and_entropies(self.actual_possibilities)).sort_values(by="entropy", ascending=False)
        return self.current_distribution.iloc[0]['word'].lower()

    def get_author(self):
        return "Mihash"
