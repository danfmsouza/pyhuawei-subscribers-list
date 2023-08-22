from abc import ABC, abstractmethod

class VLANCounterInterface(ABC):
    @abstractmethod
    def count_vlans(self, root):
        pass

    @abstractmethod
    def reset_counts(self):
        pass

    @abstractmethod
    def get_counts(self):
        pass
