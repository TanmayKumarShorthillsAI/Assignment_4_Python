from Loader_classes.FileLoader import FileLoader
import docx


class DOCXloader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path)

    def loadFile(self):
        try:
            self.loaded_file = docx.Document(self.file_path)
        except Exception as e:
            print(f"File might be corrupted: {e}")
