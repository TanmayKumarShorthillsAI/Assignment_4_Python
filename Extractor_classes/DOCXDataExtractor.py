from Extractor_classes.DataExtractor import DataExtractor


class DOCXDataExtractor(DataExtractor):
    def __init__(self, file_loader):
        super().__init__(file_loader)
        self.file_name = str(file_loader.loaded_doc).split("/")[-1].split(".")[0]
        self.text = []
        self.links = []
        self.images = []
        self.tables = []

    def extract_text(self):
        doc = self.file_loader.loaded_doc
        for para in doc.paragraphs:
            self.text.append(para.text)

        return self.text, self.file_name

    def extract_links(self):

        return self.links

    def extract_images(self):
        doc = self.file_loader.loaded_doc

        image_blobs = []

        # Loop through all relationships in the document part (images are relationships)
        for rel in doc.part.rels.values():

            if "image" in rel.target_ref:
                image_part = rel.target_part
                image_blob = image_part.blob
                image_extension = image_part.content_type.split("/")[-1]  #

                self.images.append(image_blob)
        return self.images, image_extension

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
