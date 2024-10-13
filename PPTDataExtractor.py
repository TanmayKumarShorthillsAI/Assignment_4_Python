from DataExtractor import DataExtractor


class PPTDataExtractor(DataExtractor):
    def __init__(self, file_loader):
        super().__init__(file_loader)
        self.text = []
        self.images = []
        self.links = []
        self.tables = []

    def extract_text(self):
        doc = self.file_loader.loaded_pptx

        for slide_num, slide in enumerate(doc.slides):
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    self.text.append({"slide": slide_num + 1, "text": shape.text})

        # print(self.text)
        return super().extract_text()

    def extract_links(self):
        doc = self.file_loader.loaded_pptx

        for slide_num, slide in enumerate(doc.slides):
            link = []
            for shape in slide.shapes:
                if hasattr(shape, "text_frame") and shape.text_frame is not None:
                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            if run.hyperlink:
                                link.append(run.hyperlink.address)
            self.links.append(link)

        print(self.links)
        return super().extract_links()

    def extract_images(self):
        doc = self.file_loader.loaded_pptx

        for slide_num, slide in enumerate(doc.slides):
            image = []
            for shape in slide.shapes:
                if shape.shape_type == 13:  # Shape type 13 refers to picture
                    image.append(shape.image.blob)

            self.images.append(image)

        print(self.images)
        return super().extract_images()

    def extract_tables(self):
        doc = self.file_loader.loaded_pptx

        for slide_num, slide in enumerate(doc.slides):
            temp_table = []
            for shape in slide.shapes:
                if hasattr(shape, "table"):
                    table = shape.table
                    table_data = []
                    for row in table.rows:
                        row_data = []
                        for cell in row.cells:
                            row_data.append(cell.text)
                        table_data.append(row_data)
                    temp_table.append(table_data)
            self.tables.append(temp_table)

        print(self.tables)
        return super().extract_tables()
