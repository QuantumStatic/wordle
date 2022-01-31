
from wordle import Wordle

def main():
    wordle = Wordle()
    wordle.add_try("adieu", (-1, -1, 0, -1, -1))
    wordle.add_try("minis", (-1, 1, -1, -1, -1))
    wordle.add_try("titty", (0, 1, 0, 0, -1))
    wordle.make_a_suggestion()

main()
