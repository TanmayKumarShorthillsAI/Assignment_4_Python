from abc import ABC, abstractmethod


class FileLoader(ABC):

    def __init__(self, file_path):
        self.file_path = file_path
        # self.loaded_file = None

    @abstractmethod
    def loadFile(self):
        pass
