from Storage_classes.Storage import Storage
import os
from pathlib import Path
import csv
import math


class FileStorage(Storage):
    def __init__(self, data_extractor, output_dir="output"):
        super().__init__(data_extractor)
        self.output_dir = Path(output_dir)

    def save(self):
        # store text
        text, file_name = self.data_extractor.extract_text()
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)

        text_file_path = os.path.join(self.output_dir, file_name + "_text.txt")
        with open(
            text_file_path,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(text))

        # Store images
        images, ext = self.data_extractor.extract_images()

        for i, img in enumerate(images):
            image_path = os.path.join(self.output_dir, file_name + f"_image{i}.{ext}")
            with open(image_path, "wb") as img_file:
                img_file.write(img)

        # Store links
        links = self.data_extractor.extract_links()
        links_file_path = os.path.join(self.output_dir, file_name + "_Hyperlinks.txt")
        with open(
            links_file_path,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(links))

        # Store tables
        tables = self.data_extractor.extract_tables()
        tables_file_path = os.path.join(self.output_dir, file_name + "_tables.txt")

        with open(tables_file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for table in tables:
                for row in table:
                    writer.writerow(row)
