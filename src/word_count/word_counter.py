import os
from abc import ABC, abstractmethod

import nltk

from src.word_count import Reader


def init_nltk():
    nltk_data = "punkt_tab"
    nltk_data_dir = os.path.abspath('./nltk_data')

    nltk.data.path.append(nltk_data_dir)

    try:
        nltk.data.find(f'tokenizers/{nltk_data}')
    except LookupError:
        nltk.download(nltk_data, download_dir=nltk_data_dir)


class WordCounter(ABC):
    def __init__(self):
        init_nltk()

    @abstractmethod
    def count(self, reader: Reader, threshold: int = 4) -> dict[str, int]:
        pass

