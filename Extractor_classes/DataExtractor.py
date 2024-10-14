from abc import ABC, abstractmethod
from Loader_classes.FileLoader import FileLoader


class DataExtractor(ABC):

    def __init__(self, file_loader: FileLoader):
        self.file_loader = file_loader
        self.file_loader.loadFile()
        self.file_name = str(file_loader.file_path).split("/")[-1].split(".")[0]
        self.text_metadata = []
        self.image_metadata = []
        self.text = []
        self.images = []
        self.links = []
        self.tables = []
        # print(self.file_loader.loaded_pdf)

    @abstractmethod
    def extract_text(self):
        pass

    @abstractmethod
    def extract_links(self):
        pass

    @abstractmethod
    def extract_images(self):
        pass

    @abstractmethod
    def extract_tables(self):
        pass

    @abstractmethod
    def extract_metadata(self):
        pass
