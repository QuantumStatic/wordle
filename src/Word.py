from typing import Any
from spellchecker import SpellChecker
import re


class Word(list):

    """
    Fixed Length data structure of length 5
    """

    _spell_checker = SpellChecker()

    @staticmethod
    def _assignment_validation(value, limit_length: int = 5) -> bool:
        if isinstance(value, str):
            if len(value) != limit_length:
                raise ValueError(
                    f"length doesn't match standards (expected {limit_length} got {len(value)})")
            elif re.search(r'[\W\d\s]', value) is not None:
                raise ValueError("Word contains invalid characters")

        elif isinstance(value, int):
            raise ValueError("Value must be a letter")
        elif isinstance(value, tuple) and len(value) > 5:
            raise ValueError("Word is too long")

    def __init__(self, arg=None) -> None:
        if isinstance(arg, str):
            Word._assignment_validation(arg)
            super().__init__(arg)
        else:
            super().__init__((None for _ in range(5)))

    def append(self, __object: Any) -> None:
        raise NotImplementedError("Cannot append to a word")

    def __setitem__(self, key, value):
        if value is not None:
            Word._assignment_validation(value, limit_length=1)
        return super().__setitem__(key, value)

    @property
    def is_valid(self) -> bool:
        return any(Word._spell_checker.known([''.join(self)]))

    @classmethod
    def suggest(cls, word: str) -> list:
        return tuple(filter(lambda x: len(x) == 5, cls._spell_checker.candidates(word)))

    @classmethod
    def valid(cls, word: str) -> bool:
        return any(cls._spell_checker.known(word))

    def __hash__(self) -> int:
        return hash(tuple(self))

    def match(self, word: str) -> bool:
        for x in range(5):
            if self[x] is None:
                continue
            if self[x] != word[x]:
                return False
        return True

    def __str__(self) -> str:
        return ''.join(self)


def main():
    print("Let's pass 'kince' to suggestion code")
    print("Word.suggest('kince') =", Word.suggest('kince'))
