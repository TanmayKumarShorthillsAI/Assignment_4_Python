from Extractor_classes.DataExtractor import DataExtractor
from io import BytesIO
from PIL import Image


class DOCXDataExtractor(DataExtractor):
    def __init__(self, file_loader):
        super().__init__(file_loader)
        self.file_name = str(file_loader.file_path).split("/")[-1].split(".")[0]
        self.text_metadata = []
        self.image_metadata = []
        self.text = []
        self.links = []
        self.images = []
        self.tables = []

    def is_heading(self, paragraph):
        return paragraph.style.name.startswith("Heading")

    def extract_text(self):
        doc = self.file_loader.loaded_doc
        for para in doc.paragraphs:
            self.text.append(para.text)
            # run = para.runs[0] if para.runs else None
            # # if run and run.font:
            # # font_name = run.font.name
            # # font_size = run.font.size
            # # bold = run.font.bold
            # if self.is_heading(para):
            #     self.text_metadata.append(
            #         {"Heading": {para.text}, "Level": {para.style.name}}
            #     )
        # print(self.text_metadata)
        return self.text

    def extract_links(self):

        return self.links

    def extract_images(self):
        doc = self.file_loader.loaded_doc

        # Loop through all relationships in the document part (images are relationships)
        for rel in doc.part.rels.values():

            if "image" in rel.target_ref:
                image_part = rel.target_part
                image_blob = image_part.blob
                image_stream = BytesIO(image_blob)
                image_extension = image_part.content_type.split("/")[-1]  #

                # image = Image.open(image_stream)
                # width, height = image.size
                # image_format = image.format

                # self.image_metadata.append(
                #     {
                #         "file_name": self.file_name,
                #         "image_format": image_format,
                #         "Resolution": str(width) + "x" + str(height),
                #     }
                # )
                self.images.append({"blob": image_blob, "format": image_extension})
        # print(self.image_metadata)
        return self.images

    def extract_tables(self):
        doc = self.file_loader.loaded_doc

        for table in doc.tables:
            table_text = []
            for row in table.rows:
                row_data = [cell.text for cell in row.cells]
                table_text.append(row_data)

            if len(table_text):
                self.tables.append(table_text)

        return self.tables

    def extract_metadata(self):
        doc = self.file_loader.loaded_doc
        for para in doc.paragraphs:
            run = para.runs[0] if para.runs else None
            # if run and run.font:
            # font_name = run.font.name
            # font_size = run.font.size
            # bold = run.font.bold
            if self.is_heading(para):
                self.text_metadata.append(
                    {"Heading": {para.text}, "Level": {para.style.name}}
                )

        # image metadata
        for rel in doc.part.rels.values():

            if "image" in rel.target_ref:
                image_part = rel.target_part
                image_blob = image_part.blob
                image_stream = BytesIO(image_blob)
                image_format = image_part.content_type.split("/")[-1]  #

                image = Image.open(image_stream)
                width, height = image.size
                image_format = image.format

                self.image_metadata.append(
                    {
                        "file_name": self.file_name,
                        "format": image_format,
                        "Resolution": str(width) + "x" + str(height),
                    }
                )
        return self.text_metadata, self.image_metadata
