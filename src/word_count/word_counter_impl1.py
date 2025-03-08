import nltk

from src.word_count import Reader
from src.word_count.word_counter import WordCounter


class WordCounterImpl1(WordCounter):
    def __init__(self):
        super().__init__()

    def count(self, reader: Reader, threshold: int = 4):
        counter = {}

        for line in reader.get_lines():
            words = nltk.word_tokenize(line)

            for word in words:
                if len(word) < threshold or not word.isalnum():
                    continue

                lower_word = word.lower()
                counter[lower_word] = counter.get(lower_word, 0) + 1

        return counter
