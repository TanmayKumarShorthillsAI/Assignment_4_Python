from Storage_classes.Storage import Storage
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


# class to store extarcted data(images, images_metadata and links) in MySQL database.
class SQLStorage(Storage):
    def __init__(self, data_extractor):
        super().__init__(data_extractor)

        # initialize the MySQL connection and create a cursor for the entire save method
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

    def create_tables_if_not_exists(self):
        create_tables_query = [
            """
            CREATE TABLE IF NOT EXISTS images_metadata (
                file_name VARCHAR(100),
                extension VARCHAR(255),
                resolution TEXT
            );     
        """,
            """
             CREATE TABLE IF NOT EXISTS images (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255) NOT NULL,
                image mediumblob NOT NULL,
                image_format TEXT NOT NULL
            );
        """,
            """
            CREATE TABLE IF NOT EXISTS links (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255) NOT NULL,
                url VARCHAR(500) NOT NULL
            );
        """,
        ]
        try:
            for q in create_tables_query:
                self.cursor.execute(q)
                self.connection.commit()
        except Exception as e:
            print(e)

    def insert_images(self):
        insert_images_query = """
            INSERT INTO images(file_name, image, image_format)
            VALUES (%s, %s, %s)
            """

        for x in self.images:
            values = (x["file_name"], x["blob"], x["format"])

            try:
                self.cursor.execute(insert_images_query, values)
            except Exception as e:
                print(e)

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

            try:
                self.cursor.execute(insert_links_query, values)
            except Exception as e:
                print(e)

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

            try:
                self.cursor.execute(insert_image_metadata_query, values)
            except Exception as e:
                print(e)

    def save(self):
        self.create_tables_if_not_exists()

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
