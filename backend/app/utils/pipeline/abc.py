from abc import ABC, abstractmethod

class SignalProcessor(ABC):
    def __init__(self, fs: int):
        self.fs = fs

    @abstractmethod
    def process(self, data: dict[str, object]) -> dict[str, object]:
        pass