from abc import ABC, abstractmethod
from Extractor_classes.DataExtractor import DataExtractor


class Storage(ABC):
    def __init__(self, data_extractor: DataExtractor):
        self.data_extractor = data_extractor

    @abstractmethod
    def save(self):
        pass
