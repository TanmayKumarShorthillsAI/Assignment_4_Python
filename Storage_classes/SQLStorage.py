from Storage_classes.Storage import Storage
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


class SQLStorage(Storage):
    def __init__(self, data_extractor):
        super().__init__(data_extractor)
        self.connection = mysql.connector.connect(
            host=os.getenv("host"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            database=os.getenv("database"),
        )

        self.cursor = self.connection.cursor()
        self.text = data_extractor.extract_text()
        self.text_metadata, self.image_metadata = data_extractor.extract_metadata()
        self.links = data_extractor.extract_links()
        self.images = data_extractor.extract_images()

    def insert_images(self):
        insert_images_query = """
            INSERT INTO images(file_name, image, image_format)
            VALUES (%s, %s, %s)
            """

        for x in self.images:
            values = (x["file_name"], x["blob"], x["format"])

            self.cursor.execute(insert_images_query, values)

    def insert_links(self):
        insert_links_query = """
            INSERT INTO links(file_name, url)
            VALUES (%s, %s)
            """

        for x in self.links:
            values = (
                x["file_name"],
                x["link"],
            )

            self.cursor.execute(insert_links_query, values)

    def insert_images_metadata(self):
        insert_image_metadata_query = """
            INSERT INTO images_metadata(file_name, extension, resolution)
            VALUES (%s, %s, %s)
            """

        for x in self.image_metadata:
            values = (
                x["file_name"],
                x["format"],
                x["resolution"],
            )

            self.cursor.execute(insert_image_metadata_query, values)

    def save(self):

        enter_records = [
            self.insert_images_metadata,
            self.insert_links,
            self.insert_images,
        ]

        try:

            for query in enter_records:
                query()
                self.connection.commit()
                print(f"{self.cursor.rowcount} records inserted successfully.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()

        self.cursor.close()
        self.connection.close()
