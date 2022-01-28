from myFunctions import execute_this
from Word import Word
from Feedback import Feedback
from typing import Union


class Wordle:
    def __init__(self):
        self._tries: dict[str, tuple] = {}
        self.MAX_TRIES: int = 5
        self._formulated_word = Word()
        self.letters: dict[int, Union[list, None]] = {}
        self.wrong_letters: set[str] = {"'"}
        self.misplaced_letters: set[str] = set()
        self._final_suggestions = []
        self._all_words = []
        for x in range(5):
            self.letters[x] = [chr(ord('a') + i) for i in range(26)]

    def _update_formulated_word(self, new_word: Word):
        for index in self._tries[new_word].confirmed_letters:
            self._formulated_word[index] = new_word[index]
            self.misplaced_letters.add(new_word[index])
            self.letters[index] = None
        for index in self._tries[new_word].wrongly_placed_letters:
            try:
                self.letters[index].remove(new_word[index])
                self.misplaced_letters.add(new_word[index])
            except (AttributeError, KeyError, ValueError):
                pass
        for wrong_letter_index in self._tries[new_word].wrong_letters:
            for index in range(5):
                try:
                    if new_word[wrong_letter_index] in self._formulated_word:
                        self.letters[index].remove(
                            new_word[wrong_letter_index])
                    elif new_word[wrong_letter_index] not in self.misplaced_letters:
                        self.letters[index].remove(
                            new_word[wrong_letter_index])
                        self.wrong_letters.add(new_word[wrong_letter_index])
                except (AttributeError, ValueError):
                    pass

    def add_try(self, word: str, feedback: tuple[int]) -> None:
        word = Word(word)
        self._tries[word] = Feedback(feedback)
        self._update_formulated_word(word)

    def _create_all_words(self, index: int, word: Word) -> Word:
        if index == 5:
            self._all_words.append(''.join(word))
            return
        if self.letters[index] is not None:
            for letter in self.letters[index]:
                word[index] = letter
                self._create_all_words(index + 1, word)
        elif self.letters[index] is None:
            self._create_all_words(index + 1, word)

    def _verify_word(self, word: str) -> None:
        if self._formulated_word.match(word) and not any(filter(lambda x: x in self.wrong_letters, word)) is True:
            for index, letter in enumerate(word):
                if self.letters[index] is not None and letter not in self.letters[index]:
                    return False
            if len(self.misplaced_letters.difference(set(word))) == 0:
                return True
        return False

    def make_a_suggestion(self) -> set[str]:
        if self._tries == 0:
            print("Can't make a suggestion without any try")

        suggestion_word = Word()
        for x in range(5):
            suggestion_word[x] = self._formulated_word[x]

        self._all_words.clear()
        self._create_all_words(0, suggestion_word.copy())

        self._final_suggestions = []

        suggested_words = tuple(filter(Word.valid, self._all_words))
        verified_words = tuple(filter(self._verify_word, suggested_words))
        print(*verified_words)
        self._predict(verified_words)

    def _predict(self, words: tuple[str]) -> None:
        counted = {}
        for letter in ''.join(words):
            try:
                counted[letter] += 1
            except KeyError:
                counted[letter] = 1

        strongest_word, largest_score = [], float('-inf')
        for word in words:
            temp_score = 0
            for letter in word:
                temp_score += counted[letter]
            if temp_score > largest_score:
                largest_score = temp_score
                strongest_word = [word]
            elif temp_score == largest_score:
                strongest_word.append(word)

        print("Recommended Suggestion:", end=' ')
        for word in strongest_word:
            print(word, end=' ')
        print()


@execute_this
def wordle():
    # perky
    wordle = Wordle()
    wordle.add_try("aglet", (-1, -1, -1, 0, -1))
    wordle.add_try("eerie", (-1, 1, 1, -1, -1))
    wordle.add_try("berry", (-1, 1, 1, -1, 1))
    wordle.add_try("nerdy", (-1, 1, 1, -1, 1))
    wordle.add_try("jerky", (-1, 1, 1, 1, 1))
    wordle.make_a_suggestion()
