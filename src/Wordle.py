from Word import Word
from Feedback import Feedback
from typing import Union
from DataStorage import DataStorage


class Wordle:
    def __init__(self):
        self._tries: dict[str, tuple] = {}
        self.MAX_TRIES: int = 5
        self._formulated_word = Word()
        self.letters: dict[int, Union[list, None]] = {}
        self.wrong_letters: set[str] = {"'"}
        self.misplaced_letters: set[str] = set()
        self.simple_tries: list[Word] = []
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
                        wrong_letters = tuple(map(lambda x: new_word[x],self._tries[new_word].wrongly_placed_letters))
                        if new_word[wrong_letter_index] not in wrong_letters:
                            self.letters[index].remove(new_word[wrong_letter_index])
                        else:
                            self.letters[wrong_letter_index].remove(new_word[wrong_letter_index])
                            break
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
        self.simple_tries.append(word)

    def _create_all_words(self, index: int, word: Word) -> Word:
        if index == 5:
            yield ''.join(word)
        if index != 5 and self.letters[index] is not None:
            for letter in self.letters[index]:
                word[index] = letter
                yield from self._create_all_words(index + 1, word)
        elif index != 5 and self.letters[index] is None:
            yield from self._create_all_words(index + 1, word)

    def _verify_word(self, word: str) -> None:
        if self._formulated_word.match(word) and not any(filter(lambda x: x in self.wrong_letters, word)) is True:
            for index, letter in enumerate(word):
                if self.letters[index] is not None and letter not in self.letters[index]:
                    return False
            if len(self.misplaced_letters.difference(set(word))) == 0:
                return True
        return False

    def make_a_suggestion(self, all_available_words = False, prediction = True) -> set[str]:
        if self._tries == 0:
            print("Can't make a suggestion without any try")

        if all(self._formulated_word):
            print(f"The word is {''.join(self._formulated_word)}!")
            return

        suggested_words = None
        for word in reversed(self.simple_tries):
            if DataStorage().saved(Word.get_id(word, self._tries[word])):
                suggested_words = DataStorage().load_object(Word.get_id(word, self._tries[word]))
                break
        else:
            suggested_words = filter(Word.valid, self._create_all_words(0, self._formulated_word.copy()))
        
        verified_words = tuple(filter(self._verify_word, suggested_words))
        if not DataStorage().saved(Word.get_id(self.simple_tries[-1], self._tries[self.simple_tries[-1]])):
            DataStorage().store_object(Word.get_id(self.simple_tries[-1], self._tries[self.simple_tries[-1]]), verified_words)
        if all_available_words:
            print(*verified_words)
        if prediction:
            self._predict(verified_words)

    def _predict(self, words: tuple[str]) -> None:

        if len(words) == 1:
            print(f"The code thinks the word is {words[0]}!")
            return

        counted: dict[str, int] = {}
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
