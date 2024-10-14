import pytest
from unittest.mock import patch, MagicMock
from Storage_classes.Storage import Storage
from Storage_classes import (
    SQLStorage,
)  # Replace 'your_module' with the actual module name


@pytest.fixture
def mock_data_extractor():
    """Fixture to create a mock data extractor."""
    mock_extractor = MagicMock()
    mock_extractor.extract_text.return_value = ["Sample text"]
    mock_extractor.extract_metadata.return_value = (
        [{"text": "Sample Text", "font": "Arial", "heading": True}],
        [{"file_name": "sample_image", "format": "jpeg", "resolution": "800x600"}],
    )
    mock_extractor.extract_links.return_value = ["http://example.com"]
    return mock_extractor


@patch("mysql.connector.connect")
def test_save_inserts_image_metadata(mock_connect, mock_data_extractor):
    """Test that image metadata is correctly inserted into the database."""
    # Arrange
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value = mock_cursor
    sql_storage = SQLStorage(mock_data_extractor)

    # Act
    sql_storage.save()

    # Assert
    insert_query = """
        INSERT INTO image_metadata(id, file_name, extention, resolution)
        VALUES (%s, %s, %s, %s)
    """
    assert (
        mock_cursor.execute.call_count == 1
    )  # We expect one execute call for inserting data
    mock_cursor.execute.assert_called_with(
        insert_query, (1, "sample_image", "jpeg", "800x600")
    )

    mock_cursor.rowcount = 1  # Simulate that one row was inserted successfully
    mock_cursor.connection.commit.assert_called_once()  # Commit should be called
    mock_cursor.close.assert_called_once()  # Cursor should be closed
    mock_connect.return_value.close.assert_called_once()  # Connection should be closed


@patch("mysql.connector.connect")
def test_save_handles_database_errors(mock_connect, mock_data_extractor):
    """Test that errors during database operations are handled properly."""
    # Arrange
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")

    sql_storage = SQLStorage(mock_data_extractor)

    # Act
    sql_storage.save()

    # Assert
    mock_cursor.rollback.assert_called_once()  # Rollback should be called on error
    mock_cursor.close.assert_called_once()  # Cursor should be closed
    mock_connect.return_value.close.assert_called_once()  # Connection should be closed


@patch("mysql.connector.connect")
def test_save_no_image_metadata(mock_connect, mock_data_extractor):
    """Test saving with no image metadata."""
    # Arrange
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value = mock_cursor
    mock_data_extractor.extract_metadata.return_value = ([], [])  # No image metadata
    sql_storage = SQLStorage(mock_data_extractor)

    # Act
    sql_storage.save()

    # Assert
    assert mock_cursor.execute.call_count == 0  # No execute calls for inserting data
    mock_cursor.connection.commit.assert_not_called()  # Commit should not be called
    mock_cursor.close.assert_called_once()  # Cursor should be closed
    mock_connect.return_value.close.assert_called_once()  # Connection should be closed
