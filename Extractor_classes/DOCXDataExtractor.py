from Extractor_classes.DataExtractor import DataExtractor
from io import BytesIO
from PIL import Image


class DOCXDataExtractor(DataExtractor):
    def __init__(self, file_loader):
        super().__init__(file_loader)
        self.doc = self.file_loader.loaded_doc

    def is_heading(self, paragraph):
        return paragraph.style.name.startswith("Heading")

    def extract_text(self):
        for para in self.doc.paragraphs:
            self.text.append(para.text)

        return self.text

    def extract_links(self):
        # Access the document's relationships to find hyperlinks
        for rel in self.doc.part.rels.values():
            if "hyperlink" in rel.reltype:
                hyperlink = rel.target_ref
                self.links.append({"file_name": self.file_name, "link": hyperlink})
        return self.links

    def extract_images(self):

        # Loop through all relationships in the document part (images are relationships)
        for rel in self.doc.part.rels.values():

            if "image" in rel.target_ref:
                image_part = rel.target_part
                image_blob = image_part.blob
                image_extension = image_part.content_type.split("/")[-1]  #

                self.images.append(
                    {
                        "file_name": self.file_name,
                        "blob": image_blob,
                        "format": image_extension,
                    }
                )

        return self.images

    def extract_tables(self):

        for table in self.doc.tables:
            table_text = []
            for row in table.rows:
                row_data = [cell.text for cell in row.cells]
                table_text.append(row_data)

            if len(table_text):
                self.tables.append(table_text)

        return self.tables

    def extract_metadata(self):
        for para in self.doc.paragraphs:
            run = para.runs[0] if para.runs else None
            if run and run.font:
                font_name = run.font.name
                heading = False
                if self.is_heading(para):
                    heading = True
                self.text_metadata.append(
                    {"text": para.text, "font": font_name, "heading": heading}
                )

        for rel in self.doc.part.rels.values():

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
                        "resolution": str(width) + "x" + str(height),
                    }
                )
        return self.text_metadata, self.image_metadata
