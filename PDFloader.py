from FileLoader import FileLoader
import fitz


class PDFloader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.loaded_pdf = None
        # self.loadFile()
        # print(self.loaded_pdf)

    def loadFile(self):
        self.loaded_pdf = fitz.open(self.file_path)
