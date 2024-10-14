from Storage import Storage
import _mysql_connector
from dotenv import load_dotenv
import os

load_dotenv()


class SQLStorage(Storage):
    def __init__(self, data_extractor):
        super().__init__(data_extractor)
        self.text = data_extractor.text
        self.text_metadata = data_extractor.text_metadata
        self.image_metadata = data_extractor.image_metadata
        self.links = data_extractor.links

    def save(self):
        connection = _mysql_connector.connect(
            host=os.getenv("host"),
            user=os.getenv("root"),
            password=os.getenv("password"),
            database=os.getenv("database"),
        )

        cursor = connection.cursor()

        insert_query = """
            INSERT INTO pdf_data (id, file_name, data_type, extracted_data)
            VALUES (%s, %s, %s, %s)
            """

        cursor.execute()
