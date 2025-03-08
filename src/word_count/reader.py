from typing import Generator, Literal
import os


class Reader:
    def __init__(self, file_path: str, repeat=1):
        self.file_path = file_path
        self.repeat = repeat

    def get_file_size(self, unit: Literal['byte', 'kb', 'mb', 'gb'] = 'byte') -> float:
        size_in_bytes = os.path.getsize(self.file_path) * self.repeat
        units = {'byte': 1, 'kb': 1024, 'mb': 1024 ** 2, 'gb': 1024 ** 3}
        return size_in_bytes / units[unit]

    def get_lines(self) -> Generator[str, None, None]:
        for i in range(self.repeat):
            with open(self.file_path, 'r') as file:
                for line in file:
                    if line[-1] == "\n":
                        line = line[:-1]

                    if line:
                        yield line

    def get_batches(self, batch_size: int) -> Generator[list[str], None, None]:
        current_batch = []
        current_batch_size = 0

        for line in self.get_lines():
            current_batch.append(line)
            current_batch_size += 1

            if current_batch_size >= batch_size:
                yield current_batch
                current_batch = []
                current_batch_size = 0

        if current_batch_size > 0:
            yield current_batch
