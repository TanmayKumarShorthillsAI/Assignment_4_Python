from DataExtractor import DataExtractor

# import docx


class DOCXDataExtractor(DataExtractor):
    def __init__(self, file_loader):
        super().__init__(file_loader)
        self.text = []
        self.links = []
        self.images = []
        self.tables = []

    def extract_text(self):
        doc = self.file_loader.loaded_doc
        for para in doc.paragraphs:
            self.text.append(para.text)

        # print(self.text)
        return super().extract_text()

    def extract_links(self):

        return super().extract_links()

    def extract_images(self):
        doc = self.file_loader.loaded_doc

        return super().extract_images()

    def extract_tables(self):
        # tables_data = []
        doc = self.file_loader.loaded_doc

        for table in doc.tables:
            table_text = []
            for row in table.rows:
                row_data = [cell.text for cell in row.cells]
                table_text.append(row_data)
                self.tables.append(table_text)

        # print(self.tables)
        return super().extract_tables
