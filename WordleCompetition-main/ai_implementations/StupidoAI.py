import random

import numpy as np
import pandas as pd
import itertools
import math
from WordleAI import WordleAI, LetterInformation
from WordleJudge import WordleJudge


class StupidoAI(WordleAI):

    # UNKOWN = auto()  # light grey in the game
    # PRESENT = auto()  # yellow in the game
    # NOT_PRESENT = auto()  # dark grey in the game
    # CORRECT = auto()  # green in the game
    def __init__(self, words):
        super().__init__(words)
        self.judge = WordleJudge(words)
        self._name_of_mine = "StupidoAI"

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
            self.actual_possibilities = list(pd.read_csv("../data/word_distributions.csv",
                                                              usecols=["word", "distribution", "entropy"])[:]['word'])
            return random.choice(self.actual_possibilities).lower()
        else:
            self.actual_possibilities = self.narrow_guesses(guess_history[-1])
            return random.choice(self.actual_possibilities).lower()

    def get_author(self):
        return "Mihash"
