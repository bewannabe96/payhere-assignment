import queue
import threading
from typing import List, Dict

import nltk

from src.word_count import Reader
from src.word_count.word_counter import WordCounter


class WordCounterImpl2(WordCounter):
    def __init__(self, thread_pool_size: int = 4, batch_size: int = 100):
        super().__init__()

        self._counter = {}
        self._counter_lock = threading.Lock()
        self._thread_pool_size = thread_pool_size
        self._task_queue = queue.Queue()
        self._read_complete_event = threading.Event()
        self._batch_size = batch_size

    def _worker_process(self, threshold: int):
        while True:
            try:
                batch: list[str] = self._task_queue.get(block=True, timeout=0.00001)

                local_counter: Dict[str, int] = {}

                for line in batch:
                    words = nltk.word_tokenize(line)

                    for word in words:
                        if len(word) < threshold or not word.isalnum():
                            continue

                        lower_word = word.lower()
                        local_counter[lower_word] = local_counter.get(lower_word, 0) + 1

                count_rows = local_counter.items()
                for word, count in count_rows:
                    with self._counter_lock:
                        self._counter[word] = self._counter.get(word, 0) + count

                self._task_queue.task_done()
            except queue.Empty:
                if self._read_complete_event.is_set():
                    break

    def count(self, reader: Reader, threshold: int = 4):
        self._counter = {}
        self._task_queue = queue.Queue()
        self._read_complete_event = threading.Event()

        thread_pool: List[threading.Thread] = []
        for _ in range(self._thread_pool_size):
            thread = threading.Thread(target=self._worker_process, args=(threshold,))
            thread_pool.append(thread)
            thread.start()

        for batch in reader.get_batches(self._batch_size):
            self._task_queue.put(batch)
        self._read_complete_event.set()

        self._task_queue.join()

        for thread in thread_pool:
            thread.join()

        return self._counter
