from abc import ABC, abstractmethod
from typing import Dict


class TopNPicker(ABC):
    @abstractmethod
    def pick_top_n(self, count_dict: Dict[str, int], n: int) -> list[tuple[str, int]]:
        pass
