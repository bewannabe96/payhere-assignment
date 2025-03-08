from src.word_count.top_n_picker import TopNPicker


class TopNPickerImpl1(TopNPicker):
    def pick_top_n(self, count_dict, n) -> list[tuple[str, int]]:
        return sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))[:n]
