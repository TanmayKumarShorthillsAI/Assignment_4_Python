import pytest
import fitz
import os
from Loader_classes.FileLoader import FileLoader
from Loader_classes.PDFloader import PDFloader


# Mocking fitz.open to prevent opening actual files in test cases
def test_loadFile_valid_pdf():
    pdf_loader = PDFloader(
        "/home/shtlp_0029/Desktop/Assignment_4-Python/sample_pdf.pdf"
    )
    pdf_loader.loadFile()
    assert pdf_loader.loaded_pdf.is_pdf == True


def test_loadFile_invalid_extension():
    pdf_loader = PDFloader("/home/shtlp_0029/Desktop/Assignment_4-Python/License.txt")
    with pytest.raises(TypeError) as excinfo:
        pdf_loader.loadFile()
    assert str(excinfo.value) == "Not a .pdf file. Please provide a .pdf file"
