from typing import Union


class Feedback:
    def __init__(self, values: Union[list[int], tuple[int]]):
        self._values: Union[list[int], tuple[int]] = values
        self._confirmed_letters = (
            index for index, value in enumerate(self._values) if value == 1)
        self._wrongly_placed_letters = [
            index for index, value in enumerate(self._values) if value == 0]
        self._wrong_letters = (
            index for index, value in enumerate(self._values) if value == -1)

    def __getitem__(self, key) -> int:
        return self._values[key]

    @property
    def confirmed_letters(self) -> int:
        yield from self._confirmed_letters

    @property
    def wrongly_placed_letters(self) -> int:
        yield from self._wrongly_placed_letters

    @property
    def wrong_letters(self) -> int:
        yield from self._wrong_letters

    @property
    def values(self) -> Union[list[int], tuple[int]]:
        return self._values
