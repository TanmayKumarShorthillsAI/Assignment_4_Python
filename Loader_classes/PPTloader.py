from Loader_classes.FileLoader import FileLoader
import pptx


class PPTloader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path)

    def loadFile(self):
        try:
            self.loaded_file = pptx.Presentation(self.file_path)
        except Exception as e:
            print(f"File might be corrupted: {e}")
