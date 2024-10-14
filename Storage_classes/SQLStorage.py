from Storage_classes.Storage import Storage
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


class SQLStorage(Storage):
    def __init__(self, data_extractor):
        super().__init__(data_extractor)
        self.text = data_extractor.extract_text()
        self.text_metadata, self.image_metadata = data_extractor.extract_metadata()
        # self.image_metadata = data_extractor.image_metadata
        self.links = data_extractor.extract_links()

    def save(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tanmay123",
            database="file_extracted_data",
        )
        print(connection, self.image_metadata)

        cursor = connection.cursor()

        insert_query = """
            INSERT INTO image_metadata(id, file_name, extention, resolution)
            VALUES (%s, %s, %s, %s)
            """

        try:
            for i, x in enumerate(self.image_metadata):
                values = (
                    i + 1,
                    x["file_name"],
                    x["format"],
                    x["resolution"],
                )

                cursor.execute(insert_query, values)
            connection.commit()
            print(f"{cursor.rowcount} records inserted successfully.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection.rollback()

        # Step 4: Close the cursor and the connection
        cursor.close()
        connection.close()
