import itertools
import time
from typing import List
import numpy as np
import wordle
from cli import CLIPlayer
import pandas as pd
import multiprocessing
from joblib import Parallel, delayed

class InformedPlayer(CLIPlayer):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.possible_feedback_permutations = list(itertools.product([
            wordle.LetterStates.CORRECTPOSITION,
            wordle.LetterStates.NOTPRESENT,
            wordle.LetterStates.INCORRECTPOSITION
        ], repeat=5))
        print(f"There are {len(self.game.VALID_SOLUTIONS)} valid guesses, and {len(self.game.VALID_GUESSES)} possible words")

        self.actual_possibilities = self.game.VALID_GUESSES
        self.current_distribution = pd.read_csv("data/word_distributions.csv",
                                                usecols=["word", "distribution", "entropy"])\
                                    .sort_values(by="entropy", ascending=False)
      # self.current_distribution= pd.DataFrame(self.calc_distributions_and_entropy(self.actual_possibilities)).sort_values(by="entropy",
      #                                                                                          ascending=False)

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

    def calc_distribution_and_entropy(self,word):
        dist = self.calc_word_distribution(word)
        return ({
            'word': word,
            'distribution': dist,
            'entropy': self.calc_entropy(dist)
        })

    def calc_distributions_and_entropies_parallel(self,words):
        parallel_results = Parallel(n_jobs=multiprocessing.cpu_count())(
            delayed(self.calc_distribution_and_entropy)(word) for word in words)
        return parallel_results
    def calc_distributions_and_entropies(self, words):
        result = []
        for i,w in enumerate(words):
            result.append(self.calc_distribution_and_entropy(w))
        return result

    def narrow_guesses(self, guess):
        possibilities = self.actual_possibilities
        for i, (letter, state) in enumerate(zip(list(guess[0]), guess[1])):
            if state == wordle.LetterStates.NOTPRESENT:
                possibilities = tuple(word for word in possibilities if letter not in word)
            if state == wordle.LetterStates.CORRECTPOSITION:
                possibilities = tuple(word for word in possibilities if word[i] == letter)
            if state == wordle.LetterStates.INCORRECTPOSITION:
                possibilities = tuple(word for word in possibilities if (letter in word and word[i] != letter))
        return possibilities

    def handle_response(self, guess: str, states: List[wordle.LetterStates], hint: int):
        super().handle_response(guess, states, hint)
        print()
        self.actual_possibilities = self.narrow_guesses(self._response_history[-1])
        # print("Actual possibilities")
        # print(self.actual_possibilities)
        # print(len(self.actual_possibilities), "possibilities")
        self.current_distribution = pd.DataFrame(
            self.calc_distributions_and_entropies(self.actual_possibilities)).sort_values(by="entropy", ascending=False)


# if __name__ == "__main__":
#     game = wordle.Game()
#     # game.POSSIBLE_WORDS = game.POSSIBLE_WORDS[0:1000]
#     # game.VALID_GUESSES = game.POSSIBLE_WORDS
#
#     player = MyCLIPlayer(game)
#     start_time = time.time()
#     df = pd.DataFrame(player.calc_distributions_and_entropies_parallel(player.actual_possibilities)).sort_values(by="entropy",ascending=False)
#     # print(df.head())
#     print("The time for calc dist :",
#           time.time()- start_time)
#     df.to_csv("word_distributions.csv")
#     # game.play(player, random.choice(game.VALID_SOLUTIONS))


