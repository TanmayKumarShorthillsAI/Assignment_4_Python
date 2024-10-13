from Storage import Storage
import _mysql_connector


class SQLStorage(Storage):
    def __init__(self, data_extractor):
        super().__init__(data_extractor)
        self.text = data_extractor.text

    def save(self):
        connection = _mysql_connector.connect(
            host="localhost",
            user="root",
            password="tanmay123",
            database="file_extracted_data",
        )

        cursor = connection.cursor()

        insert_query = """
            INSERT INTO pdf_data (id, file_name, data_type, extracted_data)
            VALUES (%s, %s, %s, %s)
            """

        cursor.execute()
