import pytest
from unittest.mock import Mock
from Extractor_classes.DataExtractor import DataExtractor
from Extractor_classes import DOCXDataExtractor


@pytest.fixture
def mock_file_loader():
    """Fixture to create a mock file loader."""
    return Mock()


@pytest.fixture
def docx_extractor(mock_file_loader):
    """Fixture to create a DOCXDataExtractor instance."""
    return DOCXDataExtractor(mock_file_loader)


def test_empty_docx(docx_extractor):
    """Test extraction from a blank DOCX file."""
    docx_extractor.file_loader.loaded_doc.paragraphs = []

    text = docx_extractor.extract_text()
    assert text == []  # Expecting an empty text list

    links = docx_extractor.extract_links()
    assert links == []  # Expecting an empty links list

    images = docx_extractor.extract_images()
    assert images == []  # Expecting an empty images list

    tables = docx_extractor.extract_tables()
    assert tables == []  # Expecting an empty tables list


def test_docx_with_text(docx_extractor):
    """Test extraction from a DOCX file with text."""
    docx_extractor.file_loader.loaded_doc.paragraphs = [Mock(text="Sample text")]

    text = docx_extractor.extract_text()
    assert text == ["Sample text"]  # Expecting to retrieve the sample text


def test_docx_with_links(docx_extractor):
    """Test extraction from a DOCX file with hyperlinks."""
    rel_mock = Mock()
    rel_mock.target_ref = "http://example.com"
    docx_extractor.file_loader.loaded_doc.part.rels.values.return_value = [rel_mock]

    links = docx_extractor.extract_links()
    assert links == [{"url": "http://example.com"}]  # Expecting to retrieve the link


def test_docx_with_images(docx_extractor):
    """Test extraction from a DOCX file with images."""
    image_mock = Mock()
    image_mock.blob = b"somebinarydata"
    image_mock.content_type = "image/png"
    rel_mock = Mock(target_part=image_mock)
    rel_mock.target_ref = "image.png"
    docx_extractor.file_loader.loaded_doc.part.rels.values.return_value = [rel_mock]

    images = docx_extractor.extract_images()
    assert len(images) == 1
    assert images[0]["format"] == "png"  # Expecting the image format to be png


def test_docx_with_table(docx_extractor):
    """Test extraction from a DOCX file with tables."""
    mock_table = Mock()
    mock_table.rows = [Mock(cells=[Mock(text="Row1Col1"), Mock(text="Row1Col2")])]
    docx_extractor.file_loader.loaded_doc.tables = [mock_table]

    tables = docx_extractor.extract_tables()
    assert tables == [
        [["Row1Col1", "Row1Col2"]]
    ]  # Expecting to retrieve the table data


def test_docx_with_large_text(docx_extractor):
    """Test extraction from a large DOCX file with lots of text."""
    paragraphs = [Mock(text=f"Text {i}") for i in range(1000)]
    docx_extractor.file_loader.loaded_doc.paragraphs = paragraphs

    text = docx_extractor.extract_text()
    assert len(text) == 1000  # Expecting 1000 text items


def test_docx_with_multiple_images(docx_extractor):
    """Test extraction from a DOCX file with multiple images."""
    image_mock_1 = Mock()
    image_mock_1.blob = b"image_data_1"
    image_mock_1.content_type = "image/jpeg"

    image_mock_2 = Mock()
    image_mock_2.blob = b"image_data_2"
    image_mock_2.content_type = "image/png"

    rel_mock_1 = Mock(target_part=image_mock_1)
    rel_mock_1.target_ref = "image1.jpg"

    rel_mock_2 = Mock(target_part=image_mock_2)
    rel_mock_2.target_ref = "image2.png"

    docx_extractor.file_loader.loaded_doc.part.rels.values.return_value = [
        rel_mock_1,
        rel_mock_2,
    ]

    images = docx_extractor.extract_images()
    assert len(images) == 2
    assert images[0]["format"] == "jpeg"  # Expecting the first image format to be jpeg
    assert images[1]["format"] == "png"  # Expecting the second image format to be png
