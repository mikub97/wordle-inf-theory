# Wordle Strategy Using Information Theory

This project explores the application of information theory to the popular word puzzle game, Wordle. By leveraging entropy calculations of word guesses, it aims to enhance guessing efficiency and accuracy, systematically improving game performance over the traditional random guessing strategy.

## Project Overview

Utilizing a dataset of 12,974 five-letter words, the `InformedPlayer` class implements an entropy-based strategy to select the most informative word guesses. This approach is benchmarked against a random selection strategy in a competitive setting, demonstrating the power of information theory in optimizing decision-making in Wordle.

## Features

- **InformedPlayer Class:** Implements the entropy calculation and probability distribution for each word guess based on game feedback.
- **CLI Wordle Game:** Forked and extended from [klipspringr/wordle-cli](https://github.com/klipspringr/wordle-cli), this command-line interface version of Wordle includes a comprehensive dataset of possible words and core game logic.
- **Plotly Dash Dashboard:** Provides visualizations of calculated probability distributions and entropies, offering insights into the word ranking process.

## Getting Started

### Prerequisites

- Python 3.x
- Plotly Dash
- Pandas
- NumPy

### Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/mikub97/wordle-inf-theory
cd wordle-inf-theory
pip install -r requirements.txt
```
### Usage

While playing the game in the CLI, the dashboard can be viewed in a web browser by navigating to http://127.0.0.1:8050/. This allows players to see the statistical rankings and entropies of words in real-time.

### Acknowledgments

Original CLI Wordle game by [klipspringr/wordle-cli](https://github.com/klipspringr/wordle-cli)

All contributors and participants in the [Kinkelin/WordleCompetition](https://github.com/Kinkelin/WordleCompetition)