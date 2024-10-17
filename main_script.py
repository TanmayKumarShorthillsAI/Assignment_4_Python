from Loader_classes.FileLoader import FileLoader
from Loader_classes.PDFloader import PDFloader
from Extractor_classes.PDFDataExtractor import PDFDataExtractor
from Loader_classes.DOCXloader import DOCXloader
from Extractor_classes.DOCXDataExtractor import DOCXDataExtractor
from Extractor_classes.PPTDataExtractor import PPTDataExtractor
from Loader_classes.PPTloader import PPTloader
from Storage_classes.FileStorage import FileStorage
from Storage_classes.SQLStorage import SQLStorage
import os


# common method to return the extractor class for each file format
def load_and_extract(file_path, file_extension, load_and_extract_methods):
    loader = load_and_extract_methods[f"{file_extension}"]["loader"](file_path)
    loader.loadFile()
    return load_and_extract_methods[f"{file_extension}"]["extractor"](loader)


def main():

    file_path = str(input("Enter the file path of the document:   "))
    file_extention = os.path.splitext(file_path)[1]

    # dictionary to store loader and extractors for each extension
    load_and_extract_methods = {}
    load_and_extract_methods[".pdf"] = {
        "loader": PDFloader,
        "extractor": PDFDataExtractor,
    }
    load_and_extract_methods[".docx"] = {
        "loader": DOCXloader,
        "extractor": DOCXDataExtractor,
    }
    load_and_extract_methods[".pptx"] = {
        "loader": PPTloader,
        "extractor": PPTDataExtractor,
    }

    if file_extention not in [".pdf", ".docx", ".pptx"]:
        raise TypeError("provide a .pdf, .dox or .pptx file")

    # store extracted data in directory
    file_storage = FileStorage(
        load_and_extract(file_path, file_extention, load_and_extract_methods)
    )
    file_storage.save()

    # store extracted data in database
    permission = str(
        input(
            "Press [Y/y] to store the extracted image, image_metadata, and links in database else press [N/n]:  "
        )
    )
    if permission == "Y" or permission == "y":
        sql_storage = SQLStorage(
            load_and_extract(file_path, file_extention, load_and_extract_methods)
        )
        sql_storage.save()


if __name__ == "__main__":
    main()
