from abc import ABC, abstractmethod


# Abstarct class for loading a file
class FileLoader(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
        self.loaded_file = None

    @abstractmethod
    def loadFile(self):
        pass
