import pytest
from Loader_classes.FileLoader import FileLoader
from Loader_classes.DOCXloader import DOCXloader


# Mocking fitz.open to prevent opening actual files in test cases
def test_loadFile_valid_docx():
    docx_loader = DOCXloader("/home/shtlp_0029/Desktop/Assignment_4-Python/demo.docx")
    docx_loader.loadFile()
    assert docx_loader.file_extention == ".docx"


def test_loadFile_invalid_extension():
    docx_loader = DOCXloader("/home/shtlp_0029/Desktop/Assignment_4-Python/License.txt")
    with pytest.raises(TypeError) as excinfo:
        docx_loader.loadFile()
    assert str(excinfo.value) == "Not a .docx file. Please provide a .docx file"
