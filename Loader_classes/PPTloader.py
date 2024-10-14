from Loader_classes.FileLoader import FileLoader
import pptx
import os


class PPTloader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.loaded_pptx = None
        self.file_extention = os.path.splitext(file_path)[1]

    def loadFile(self):
        if self.file_extention != ".pptx":
            raise TypeError("Not a .pptx file. Please provide a .pptx file")
        self.loaded_pptx = pptx.Presentation(self.file_path)
