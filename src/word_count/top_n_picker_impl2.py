import heapq

from src.word_count.top_n_picker import TopNPicker


class TopNPickerImpl2(TopNPicker):
    def pick_top_n(self, count_dict, n) -> list[tuple[str, int]]:
        return heapq.nsmallest(n, count_dict.items(), key=lambda x: (-x[1], x[0]))
