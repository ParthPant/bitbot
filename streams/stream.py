from typing import Callable, Optional


class Stream:
    def __init__(self):
        self.on_recv: Optional[Callable] = None

    def run_forever(self):
        pass
