import pytest
from unittest.mock import Mock
from Extractor_classes.DataExtractor import DataExtractor
from Extractor_classes import (
    PDFDataExtractor,
)  # Replace 'your_module' with the actual module name

import tabula


@pytest.fixture
def mock_file_loader():
    """Fixture to create a mock file loader."""
    return Mock()


@pytest.fixture
def pdf_extractor(mock_file_loader):
    """Fixture to create a PDFDataExtractor instance."""
    return PDFDataExtractor(mock_file_loader)


def test_empty_pdf(pdf_extractor):
    """Test extraction from a blank PDF file."""
    mock_pdf = Mock()
    mock_pdf.page_count = 0
    pdf_extractor.file_loader.loaded_pdf = mock_pdf

    text = pdf_extractor.extract_text()
    assert text == []  # Expecting an empty text list

    links = pdf_extractor.extract_links()
    assert links == []  # Expecting an empty links list

    images = pdf_extractor.extract_images()
    assert images == []  # Expecting an empty images list

    tables = pdf_extractor.extract_tables()
    assert tables == []  # Expecting an empty tables list


def test_pdf_with_text(pdf_extractor):
    """Test extraction from a PDF file with text."""
    mock_pdf = Mock()
    mock_pdf.page_count = 1
    mock_page = Mock()
    mock_page.get_text.return_value = "Sample text"
    mock_pdf.load_page.return_value = mock_page
    pdf_extractor.file_loader.loaded_pdf = mock_pdf

    text = pdf_extractor.extract_text()
    assert text == ["Sample text"]  # Expecting to retrieve the sample text


def test_pdf_with_links(pdf_extractor):
    """Test extraction from a PDF file with hyperlinks."""
    mock_pdf = Mock()
    mock_pdf.page_count = 1
    mock_page = Mock()
    mock_page.get_links.return_value = [{"uri": "http://example.com"}]
    mock_pdf.load_page.return_value = mock_page
    pdf_extractor.file_loader.loaded_pdf = mock_pdf

    links = pdf_extractor.extract_links()
    assert links == ["http://example.com"]  # Expecting to retrieve the link


def test_pdf_with_images(pdf_extractor):
    """Test extraction from a PDF file with images."""
    mock_pdf = Mock()
    mock_pdf.page_count = 1
    mock_page = Mock()
    mock_image_data = {
        "image": b"somebinarydata",
        "ext": "png",
        "width": 100,
        "height": 100,
    }
    mock_page.get_images.return_value = [(1, 0, 0, 0)]  # XREF for the image
    mock_page.extract_image.return_value = mock_image_data
    mock_pdf.load_page.return_value = mock_page
    pdf_extractor.file_loader.loaded_pdf = mock_pdf

    images = pdf_extractor.extract_images()
    assert len(images) == 1
    assert images[0]["format"] == "png"  # Expecting the image format to be png


def test_pdf_with_tables(pdf_extractor):
    """Test extraction from a PDF file with tables."""
    mock_pdf = Mock()
    mock_pdf.page_count = 1
    pdf_extractor.file_loader.file_path = "mock_path.pdf"  # Set the path for tabula
    tabula.read_pdf = Mock(
        return_value=[Mock(columns=["A", "B"], values=[[1, 2], [3, 4]])]
    )

    tables = pdf_extractor.extract_tables()
    assert len(tables) == 1
    assert tables[0] == [["A", "B"], [1, 2], [3, 4]]  # Expecting the extracted table


def test_pdf_with_large_text(pdf_extractor):
    """Test extraction from a large PDF file with lots of text."""
    mock_pdf = Mock()
    mock_pdf.page_count = 1000
    mock_page = Mock()
    mock_page.get_text.return_value = "Sample text on page"
    mock_pdf.load_page.side_effect = [
        mock_page
    ] * 1000  # Return the same mock page for each call
    pdf_extractor.file_loader.loaded_pdf = mock_pdf

    text = pdf_extractor.extract_text()
    assert len(text) == 1000  # Expecting 1000 text items


def test_pdf_with_multiple_images(pdf_extractor):
    """Test extraction from a PDF file with multiple images."""
    mock_pdf = Mock()
    mock_pdf.page_count = 1
    mock_page = Mock()
    mock_image_data_1 = {
        "image": b"image_data_1",
        "ext": "jpeg",
        "width": 100,
        "height": 200,
    }
    mock_image_data_2 = {
        "image": b"image_data_2",
        "ext": "png",
        "width": 150,
        "height": 250,
    }
    mock_page.get_images.return_value = [(1, 0, 0, 0), (2, 0, 0, 0)]  # XREFs for images
    mock_page.extract_image.side_effect = [mock_image_data_1, mock_image_data_2]
    mock_pdf.load_page.return_value = mock_page
    pdf_extractor.file_loader.loaded_pdf = mock_pdf

    images = pdf_extractor.extract_images()
    assert len(images) == 2
    assert images[0]["format"] == "jpeg"  # Expecting the first image format to be jpeg
    assert images[1]["format"] == "png"  # Expecting the second image format to be png


def test_pdf_with_metadata(pdf_extractor):
    """Test extraction of metadata from a PDF file."""
    mock_pdf = Mock()
    mock_pdf.page_count = 1
    mock_page = Mock()
    mock_page.get_text.return_value = {
        "blocks": [
            {
                "lines": [
                    {"spans": [{"text": "Heading", "font": "Helvetica", "size": 18}]}
                ]
            }
        ]
    }

    mock_pdf.load_page.return_value = mock_page
    pdf_extractor.file_loader.loaded_pdf = mock_pdf

    text_metadata, image_metadata = pdf_extractor.extract_metadata()

    assert len(text_metadata) == 1
    assert text_metadata[0]["text"] == "Heading"
    assert text_metadata[0]["font"] == "Helvetica"
    assert (
        text_metadata[0]["heading"] is True
    )  # Expecting it to be recognized as a heading
