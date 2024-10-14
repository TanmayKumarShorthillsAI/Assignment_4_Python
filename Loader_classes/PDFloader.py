from Loader_classes.FileLoader import FileLoader
import fitz
import os


class PDFloader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.loaded_pdf = None
        self.file_extention = os.path.splitext(file_path)[1]

    def loadFile(self):
        if self.file_extention != ".pdf":
            raise TypeError("Not a .pdf file. Please provide a .pdf file")
        self.loaded_pdf = fitz.open(self.file_path)
