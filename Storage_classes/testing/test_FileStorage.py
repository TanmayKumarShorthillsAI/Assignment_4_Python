import pytest
from unittest.mock import Mock, patch, MagicMock
from Storage_classes.Storage import Storage
from Storage_classes import (
    FileStorage,
)  # Replace 'your_module' with the actual module name


@pytest.fixture
def mock_data_extractor():
    """Fixture to create a mock data extractor."""
    return Mock()


@pytest.fixture
def file_storage(mock_data_extractor):
    """Fixture to create a FileStorage instance."""
    return FileStorage(mock_data_extractor, output_dir="test_output")


@patch("pathlib.Path.mkdir")
@patch("builtins.open", new_callable=MagicMock)
def test_save_metadata(mock_open, mock_mkdir, file_storage):
    """Test saving metadata, text, images, links, and tables."""
    # Mocking the data extractor methods
    mock_data_extractor.extract_metadata.return_value = (
        [{"text": "Sample Text", "font": "Arial", "heading": True}],
        [{"file_name": "sample_image", "format": "jpeg", "resolution": "800x600"}],
    )

    mock_data_extractor.extract_text.return_value = ["Sample text"]
    mock_data_extractor.extract_images.return_value = [
        {"blob": b"image_blob_data", "format": "jpeg"}
    ]
    mock_data_extractor.extract_links.return_value = ["http://example.com"]
    mock_data_extractor.extract_tables.return_value = [
        [["Header1", "Header2"], ["Row1Col1", "Row1Col2"]]
    ]

    # Mocking file paths
    mock_data_extractor.file_loader.file_path = "test/sample_file.pptx"

    file_storage.save()

    # Check metadata files were created
    assert (
        mock_open.call_count == 5
    )  # Expecting 5 open calls for text, images, links, and tables
    assert mock_mkdir.called  # Expecting the output directory to be created

    # Check if text metadata was saved correctly
    text_metadata_file_path = "test_output/sample_file_text_metadata.txt"
    mock_open.assert_any_call(text_metadata_file_path, "w", encoding="utf-8")
    handle = mock_open()
    handle.write.assert_any_call(
        "[{'text': 'Sample Text', 'font': 'Arial', 'heading': True}]"
    )

    # Check if image metadata was saved correctly
    image_metadata_file_path = "test_output/sample_file_image_metadata.txt"
    mock_open.assert_any_call(image_metadata_file_path, "w", encoding="utf-8")
    handle.write.assert_any_call(
        "[{'file_name': 'sample_image', 'format': 'jpeg', 'resolution': '800x600'}]"
    )

    # Check if text was saved correctly
    text_file_path = "test_output/sample_file_text.txt"
    mock_open.assert_any_call(text_file_path, "w", encoding="utf-8")
    handle.write.assert_any_call("['Sample text']")

    # Check if links were saved correctly
    links_file_path = "test_output/sample_file_Hyperlinks.txt"
    mock_open.assert_any_call(links_file_path, "w", encoding="utf-8")
    handle.write.assert_any_call("['http://example.com']")

    # Check if tables were saved correctly
    tables_file_path = "test_output/sample_file_tables.csv"
    mock_open.assert_any_call(tables_file_path, "w", newline="")

    # Check that CSV writer wrote the correct data
    writer = mock_open()
    writer().writerow.assert_any_call(["Header1", "Header2"])
    writer().writerow.assert_any_call(["Row1Col1", "Row1Col2"])


@patch("pathlib.Path.mkdir")
@patch("builtins.open", new_callable=MagicMock)
def test_save_no_images(mock_open, mock_mkdir, file_storage):
    """Test saving with no images."""
    # Mocking the data extractor methods
    mock_data_extractor.extract_metadata.return_value = (
        [{"text": "Sample Text", "font": "Arial", "heading": True}],
        [],
    )

    mock_data_extractor.extract_text.return_value = ["Sample text"]
    mock_data_extractor.extract_images.return_value = []  # No images
    mock_data_extractor.extract_links.return_value = ["http://example.com"]
    mock_data_extractor.extract_tables.return_value = [
        [["Header1", "Header2"], ["Row1Col1", "Row1Col2"]]
    ]

    mock_data_extractor.file_loader.file_path = "test/sample_file.pptx"

    file_storage.save()

    # Check metadata files were created
    assert mock_open.call_count == 4  # No images means 4 open calls instead of 5

    # Check if images were not saved
    mock_open.assert_any_call(
        "test_output/sample_file_image_metadata.txt", "w", encoding="utf-8"
    )
    assert not mock_open().write.call_args_list  # Expecting no writes for images


# Additional tests can be added here for other scenarios, such as missing output directory, etc.
