import random
from enum import Enum


class GameState(Enum):
    IN_PROGRESS = 0
    WON = 1
    LOST = 2


class GuessResult(Enum):
    CORRECT = 0
    INCORRECT = 1

    FAIL_INVALID_INPUT = 2
    FAIL_ALREADY_GAME_OVER = 3
    FAIL_ALREADY_GUESSED = 4


class HangmanGame:
    def __init__(self, word, failed_guesses_limit):
        if failed_guesses_limit <= 0:
            raise ValueError("failed_guesses_limit must be over 0")

        if len(word) <= 0:
            raise ValueError("word must have at least 1 letter")

        self.word = word

        self.state = GameState.IN_PROGRESS
        self.guesses = []
        self.failed_guess_limit = failed_guesses_limit
        self.num_failed_guesses_remaining = failed_guesses_limit
        self.revealed_word = "".join(["_" for i in range(len(word))])
        self.num_revealed_letters = 0

    def guess(self, input_letter):
        # FAIL, GAME ALREADY OVER
        if self.state==1 or self.state==2:
            return GuessResult.FAIL_ALREADY_GAME_OVER
        
        # INVALID INPUT
        if not input_letter.isalnum() or len(input_letter)!=1: # valid words are alphanumeric // assumption based on words in create_hangman_game()
            return GuessResult.FAIL_INVALID_INPUT

        # FAIL ALREADY GUESSED
        if input_letter in self.guesses:
            return GuessResult.FAIL_ALREADY_GUESSED

        # INCORRECT GUESS
        if input_letter not in self.word:
            #update game state
            self.guesses.append(input_letter)
            self.num_failed_guesses_remaining-=1

            # GAME LOST
            if self.num_failed_guesses_remaining<1:
                self.state=GameState.LOST 
            
            return GuessResult.INCORRECT

        # CORRECT
        else:
            #update game state
            self.guesses.append(input_letter)
            self.num_revealed_letters+=self.word.count(input_letter)

            revealed_word=[] #update revealed word
            for char in self.word:
                if char in self.guesses:
                    revealed_word.append(char)
                else:
                    revealed_word.append("_")
            self.revealed_word="".join(revealed_word)
                        
            #GAME WON
            if self.num_revealed_letters==len(self.word):
                self.state=GameState.WON
            #else: no need to update because self.state==GameState.IN_PROGRESS

            return GuessResult.CORRECT


class HangmanGameScorer:
    POINTS_PER_LETTER = 20
    POINTS_PER_REMAINING_GUESS = 10

    @classmethod
    def score(cls, game):
        points = game.num_revealed_letters * HangmanGameScorer.POINTS_PER_LETTER
        points += (
            game.num_failed_guesses_remaining
            * HangmanGameScorer.POINTS_PER_REMAINING_GUESS
        )
        return points


def create_hangman_game(words=None, guess_limit=5):
    if words is None:
        words = ["3dhubs", "marvin", "print", "filament", "order", "layer"]

    if len(words) <= 0:
        raise ValueError("words must have at least 1 word")

    if guess_limit <= 0:
        raise ValueError("guess_limit must be greater than 0")

    rand_word = words[random.randint(0, len(words) - 1)]
    return HangmanGame(rand_word, guess_limit)
