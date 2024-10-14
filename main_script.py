from Loader_classes.FileLoader import FileLoader
from Loader_classes.PDFloader import PDFloader
from Extractor_classes.PDFDataExtractor import PDFDataExtractor
from Loader_classes.DOCXloader import DOCXloader
from Extractor_classes.DOCXDataExtractor import DOCXDataExtractor
from Extractor_classes.PPTDataExtractor import PPTDataExtractor
from Loader_classes.PPTloader import PPTloader
from Storage_classes.FileStorage import FileStorage
import os
from Storage_classes.SQLStorage import SQLStorage

file_path = str(input("Enter the file path of the document:   "))


def load_and_extract_pdf():
    pdf_loader = PDFloader(file_path)
    pdf_loader.loadFile()
    return PDFDataExtractor(pdf_loader)


def load_and_extract_docx():
    docx_loader = DOCXloader(file_path)
    docx_loader.loadFile()
    return DOCXDataExtractor(docx_loader)


def load_and_extract_pptx():
    ppt_loader = PPTloader(file_path)
    ppt_loader.loadFile()
    return PPTDataExtractor(ppt_loader)


if os.path.splitext(file_path)[1] == ".pdf":
    pdf_file_storage = FileStorage(load_and_extract_pdf())
    pdf_file_storage.save()
    sql_storage = SQLStorage(load_and_extract_pdf())
    sql_storage.save()

if os.path.splitext(file_path)[1] == ".docx":
    docx_file_storage = FileStorage(load_and_extract_docx())
    docx_file_storage.save()
    sql_storage = SQLStorage(load_and_extract_docx())
    sql_storage.save()

if os.path.splitext(file_path)[1] == ".pptx":
    pptx_file_storage = FileStorage(load_and_extract_pptx())
    pptx_file_storage.save()
    sql_storage = SQLStorage(load_and_extract_pptx())
    sql_storage.save()


# sql_storage = SQLStorage(pdf_extractor)
# sql_storage.save()
