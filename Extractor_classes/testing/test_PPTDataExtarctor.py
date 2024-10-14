import pytest
from unittest.mock import Mock
from Extractor_classes.DataExtractor import DataExtractor
from Extractor_classes import (
    PPTDataExtractor,
)  # Replace 'your_module' with the actual module name


@pytest.fixture
def mock_file_loader():
    """Fixture to create a mock file loader."""
    return Mock()


@pytest.fixture
def ppt_extractor(mock_file_loader):
    """Fixture to create a PPTDataExtractor instance."""
    return PPTDataExtractor(mock_file_loader)


def test_empty_ppt(ppt_extractor):
    """Test extraction from a blank PPT file."""
    mock_ppt = Mock()
    mock_ppt.slides = []
    ppt_extractor.file_loader.loaded_pptx = mock_ppt

    text = ppt_extractor.extract_text()
    assert text == []  # Expecting an empty text list

    links = ppt_extractor.extract_links()
    assert links == []  # Expecting an empty links list

    images = ppt_extractor.extract_images()
    assert images == []  # Expecting an empty images list

    tables = ppt_extractor.extract_tables()
    assert tables == []  # Expecting an empty tables list


def test_ppt_with_text(ppt_extractor):
    """Test extraction from a PPT file with text."""
    mock_ppt = Mock()
    mock_slide = Mock()
    mock_slide.shapes = [Mock(text="Slide Title"), Mock(text="Slide Content")]
    mock_ppt.slides = [mock_slide]
    ppt_extractor.file_loader.loaded_pptx = mock_ppt

    text = ppt_extractor.extract_text()
    assert text == [
        "Slide Title",
        "Slide Content",
    ]  # Expecting to retrieve the slide text


def test_ppt_with_links(ppt_extractor):
    """Test extraction from a PPT file with hyperlinks."""
    mock_ppt = Mock()
    mock_slide = Mock()
    mock_shape = Mock()
    mock_shape.text_frame = Mock()
    mock_shape.text_frame.paragraphs = [
        Mock(runs=[Mock(hyperlink=Mock(address="http://example.com"))])
    ]
    mock_slide.shapes = [mock_shape]
    mock_ppt.slides = [mock_slide]
    ppt_extractor.file_loader.loaded_pptx = mock_ppt

    links = ppt_extractor.extract_links()
    assert links == ["http://example.com"]  # Expecting to retrieve the link


def test_ppt_with_images(ppt_extractor):
    """Test extraction from a PPT file with images."""
    mock_ppt = Mock()
    mock_slide = Mock()
    mock_shape = Mock()
    mock_shape.shape_type = 13  # Shape type for images
    mock_shape.image = Mock(blob=b"somebinarydata", ext="jpeg")
    mock_slide.shapes = [mock_shape]
    mock_ppt.slides = [mock_slide]
    ppt_extractor.file_loader.loaded_pptx = mock_ppt

    images = ppt_extractor.extract_images()
    assert len(images) == 1
    assert images[0]["format"] == "jpeg"  # Expecting the image format to be jpeg


def test_ppt_with_tables(ppt_extractor):
    """Test extraction from a PPT file with tables."""
    mock_ppt = Mock()
    mock_slide = Mock()
    mock_shape = Mock()
    mock_shape.table = Mock(
        rows=[Mock(cells=[Mock(text="Cell 1"), Mock(text="Cell 2")])]
    )
    mock_slide.shapes = [mock_shape]
    mock_ppt.slides = [mock_slide]
    ppt_extractor.file_loader.loaded_pptx = mock_ppt

    tables = ppt_extractor.extract_tables()
    assert len(tables) == 1
    assert tables[0] == [["Cell 1", "Cell 2"]]  # Expecting the extracted table


def test_ppt_with_metadata(ppt_extractor):
    """Test extraction of metadata from a PPT file."""
    mock_ppt = Mock()
    mock_slide = Mock()
    mock_shape = Mock()
    mock_shape.has_text_frame = True
    mock_shape.text_frame = Mock(
        paragraphs=[
            Mock(runs=[Mock(text="Title", font=Mock(name="Arial", size=24, bold=True))])
        ]
    )
    mock_slide.shapes = [mock_shape]
    mock_ppt.slides = [mock_slide]
    ppt_extractor.file_loader.loaded_pptx = mock_ppt

    text_metadata, image_metadata = ppt_extractor.extract_metadata()

    assert len(text_metadata) == 1
    assert text_metadata[0]["text"] == "Title"
    assert text_metadata[0]["font"] == "Arial"
    assert (
        text_metadata[0]["heading"] is True
    )  # Expecting it to be recognized as a heading
