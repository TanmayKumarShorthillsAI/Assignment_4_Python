from Storage_classes.Storage import Storage
import os
from pathlib import Path
import csv


class FileStorage(Storage):
    def __init__(self, data_extractor, output_dir="output"):
        super().__init__(data_extractor)
        self.output_dir = Path(output_dir)
        self.file_name = (
            str(self.data_extractor.file_loader.file_path).split("/")[-1].split(".")[0]
        )

    def save(self):
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)
        # Store metadata
        text_metadata, image_metadata = self.data_extractor.extract_metadata()
        # print(text_metadata, image_metadata)
        text_metadata_file_path = os.path.join(
            self.output_dir, self.file_name + "_text_metadata.txt"
        )
        with open(
            text_metadata_file_path,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(text_metadata))

        image_metadata_file_path = os.path.join(
            self.output_dir, self.file_name + "_image_metadata.txt"
        )
        with open(
            image_metadata_file_path,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(image_metadata))

        # store text
        text = self.data_extractor.extract_text()

        text_file_path = os.path.join(self.output_dir, self.file_name + "_text.txt")
        with open(
            text_file_path,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(text))

        # Store images
        images = self.data_extractor.extract_images()
        # print(len(images))
        for i, img in enumerate(images):
            # print(image_metadata[i])
            image_path = os.path.join(
                self.output_dir,
                self.file_name + f"_image{i}.{img['format']}",
            )
            with open(image_path, "wb") as img_file:
                img_file.write(img["blob"])

        # Store links
        links = self.data_extractor.extract_links()
        links_file_path = os.path.join(
            self.output_dir, self.file_name + "_Hyperlinks.txt"
        )
        with open(
            links_file_path,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(links))

        # Store tables
        tables = self.data_extractor.extract_tables()
        tables_file_path = os.path.join(self.output_dir, self.file_name + "_tables.csv")

        with open(tables_file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for table in tables:
                for row in table:
                    writer.writerow(row)
