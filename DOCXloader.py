from FileLoader import FileLoader
import docx


class PDFloader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.loaded_doc = None

    def loadFile(self):
        self.loaded_doc = docx.Document(self.file_path)
