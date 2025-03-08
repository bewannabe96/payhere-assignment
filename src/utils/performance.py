import time
from dataclasses import dataclass, field
from functools import wraps
from typing import Dict


@dataclass
class PerformanceStats:
    exec_times: list[float] = field(default_factory=lambda: [])

    call_count: int = 0
    total_time: float = 0.0
    max_time: float = float('-inf')
    min_time: float = float('inf')

    @property
    def avg_time(self) -> float:
        return self.total_time / self.call_count if self.call_count > 0 else 0.0

    @property
    def avg_time_p50(self) -> float:
        if len(self.exec_times) == 0:
            return 0

        sorted_values = sorted(self.exec_times)
        lower_bound = int(len(sorted_values) * 0.25)
        upper_bound = int(len(sorted_values) * 0.75)
        
        target_values = sorted_values[lower_bound:upper_bound+1]
        return sum(target_values) / len(target_values) if len(target_values) > 0 else 0.0

    def update(self, execution_time: float) -> None:
        self.exec_times.append(execution_time)
        self.call_count += 1
        self.total_time += execution_time
        self.max_time = max(self.max_time, execution_time)
        self.min_time = min(self.min_time, execution_time)

    def __str__(self) -> str:
        value = ""
        value += f"Count:\t\t\t{self.call_count}\n"
        value += f"Total Time:\t\t{self.total_time:.3f} ms\n"
        value += f"Average Time:\t{self.avg_time:.3f} ms\n"
        value += f"Max Time:\t\t{self.max_time:.3f} ms\n"
        value += f"Min Time:\t\t{self.min_time:.3f} ms"
        return value


class PerformanceMonitor:
    def __init__(self):
        self._stats: Dict[str, PerformanceStats] = {}

    def get_stats(self, name: str) -> PerformanceStats:
        if name not in self._stats:
            self._stats[name] = PerformanceStats()
        return self._stats[name]

    def update_stats(self, name: str, execution_time: float) -> None:
        stats = self.get_stats(name)
        stats.update(execution_time)

    def print_stats(self, name: str) -> None:
        print("+------------------------------------------+")
        print(f"[{name}]")
        print(self.get_stats(name))
        print("+------------------------------------------+")


def monitor_performance(pm: PerformanceMonitor, name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            execution_time = (end_time - start_time) * 1000

            pm.update_stats(name, execution_time)

            return result

        return wrapper

    return decorator
