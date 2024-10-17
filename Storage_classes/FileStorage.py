from Storage_classes.Storage import Storage
import os
from pathlib import Path
import csv


class FileStorage(Storage):
    def __init__(self, data_extractor, output_dir="output"):
        super().__init__(data_extractor)
        self.output_dir = Path(output_dir)
        self.output_sub_dirs = ["text", "images", "tables", "links", "metadata"]
        self.file_name = (
            str(self.data_extractor.file_loader.file_path).split("/")[-1].split(".")[0]
        )

    def save_metadata(self):
        text_metadata, image_metadata = self.data_extractor.extract_metadata()
        metadata_storage_dir = os.path.join(self.output_dir, "metadata")

        text_metadata_file_path = os.path.join(
            metadata_storage_dir, self.file_name + "_text_metadata.txt"
        )
        with open(
            text_metadata_file_path,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(text_metadata))

        image_metadata_file_path = os.path.join(
            metadata_storage_dir, self.file_name + "_image_metadata.txt"
        )
        with open(
            image_metadata_file_path,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(image_metadata))

        print("Metadata Extracted in output directory")

    def save_text(self):
        text = self.data_extractor.extract_text()

        text_storage_dir = os.path.join(self.output_dir, "text")
        text_file_path = os.path.join(text_storage_dir, self.file_name + "_text.txt")
        with open(
            text_file_path,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(text))

        print("Text Extracted in output directory")

    def save_images(self):
        images_storage_dir = os.path.join(self.output_dir, "images")

        images = self.data_extractor.extract_images()
        for i, img in enumerate(images):
            image_path = os.path.join(
                images_storage_dir,
                self.file_name + f"_image{i}.{img['format']}",
            )
            with open(image_path, "wb") as img_file:
                img_file.write(img["blob"])

        print("Images Extracted in output directory")

    def save_links(self):
        links_storage_dir = os.path.join(self.output_dir, "links")

        links = self.data_extractor.extract_links()
        links_file_path = os.path.join(
            links_storage_dir, self.file_name + "_Hyperlinks.txt"
        )
        with open(
            links_file_path,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(links))

        print("Links Extracted in output directory")

    def save_tables(self):
        tables_storage_dir = os.path.join(self.output_dir, "tables")

        tables = self.data_extractor.extract_tables()
        tables_file_path = os.path.join(
            tables_storage_dir, self.file_name + "_tables.csv"
        )

        with open(tables_file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for table in tables:
                for row in table:
                    writer.writerow(row)

        print("Tables Extracted in output directory")

    def save(self):
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)
        for sub_dir in self.output_sub_dirs:
            os.makedirs(os.path.join(self.output_dir, sub_dir), exist_ok=True)

        # Store metadata
        self.save_metadata()

        # store text
        self.save_text()

        # Store images
        self.save_images()

        # Store links
        self.save_links()

        # Store tables
        self.save_tables()
