from Loader_classes.FileLoader import FileLoader
import pptx


class PPTloader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.loaded_pptx = None

    def loadFile(self):
        self.loaded_pptx = pptx.Presentation(self.file_path)
