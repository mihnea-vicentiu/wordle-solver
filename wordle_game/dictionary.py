from wordle_game.paths import WORD_LIST_FILE


def load_words():
      with WORD_LIST_FILE.open("r", encoding="utf-8") as words_file:
            return [line.strip() for line in words_file if line.strip()]


wordle_dictionary = load_words()
