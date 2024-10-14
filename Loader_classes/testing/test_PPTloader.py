import pytest
from Loader_classes.FileLoader import FileLoader
from Loader_classes.PPTloader import PPTloader


# Mocking fitz.open to prevent opening actual files in test cases
def test_loadFile_valid_pptx():
    pptx_loader = PPTloader(
        "/home/shtlp_0029/Desktop/Assignment_4-Python/Networks.pptx"
    )
    pptx_loader.loadFile()
    assert pptx_loader.file_extention == ".pptx"


def test_loadFile_invalid_extension():
    pptx_loader = PPTloader("/home/shtlp_0029/Desktop/Assignment_4-Python/License.txt")
    with pytest.raises(TypeError) as excinfo:
        pptx_loader.loadFile()
    # assert str(excinfo.value) == "Not a . file. Please provide a .docx file"
