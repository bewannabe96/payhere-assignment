import multiprocessing as mp
from typing import Generator, Dict, Tuple

import nltk

from src.word_count import Reader
from src.word_count.word_counter import WordCounter


class WordCounterImpl3(WordCounter):
    def __init__(self, process_pool_size: int = 4, batch_size: int = 100):
        super().__init__()

        self._process_pool_size = process_pool_size
        self._batch_size = batch_size

    @staticmethod
    def _worker_process(args: Tuple[list[str], int]):
        batch, threshold = args

        counter: Dict[str, int] = {}

        for line in batch:
            words = nltk.word_tokenize(line)

            for word in words:
                if len(word) < threshold or not word.isalnum():
                    continue

                lower_word = word.lower()
                counter[lower_word] = counter.get(lower_word, 0) + 1

        return counter

    def count(self, reader: Reader, threshold: int = 4):
        with mp.Pool(processes=self._process_pool_size) as pool:
            results = pool.map(
                WordCounterImpl3._worker_process,
                [(batch, threshold) for batch in reader.get_batches(self._batch_size)]
            )

        counter = {}
        for result in results:
            count_rows = result.items()
            for word, count in count_rows:
                counter[word] = counter.get(word, 0) + count

        return counter
