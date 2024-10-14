from Loader_classes.FileLoader import FileLoader
import docx
import os


class DOCXloader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path)
        # self.file_path = self.file_path
        self.file_extention = os.path.splitext(file_path)[1]
        # self.file_ext = self.file_path
        self.loaded_doc = None

    def loadFile(self):
        if self.file_extention != ".docx":
            raise TypeError("Not a .docx file. Please provide a .docx file")
        self.loaded_doc = docx.Document(self.file_path)
        # print(self.loaded_doc)
