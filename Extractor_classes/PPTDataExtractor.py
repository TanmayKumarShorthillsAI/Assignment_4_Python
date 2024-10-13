from Extractor_classes.DataExtractor import DataExtractor


class PPTDataExtractor(DataExtractor):
    def __init__(self, file_loader):
        super().__init__(file_loader)
        self.file_name = str(file_loader.loaded_pptx).split("/")[-1].split(".")[0]
        self.text = []
        self.images = []
        self.links = []
        self.tables = []

    def extract_text(self):
        doc = self.file_loader.loaded_pptx

        for slide_num, slide in enumerate(doc.slides):
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    self.text.append(shape.text)

        # print(self.text)
        return self.text, self.file_name

    def extract_links(self):
        doc = self.file_loader.loaded_pptx

        for slide_num, slide in enumerate(doc.slides):
            for shape in slide.shapes:
                if hasattr(shape, "text_frame") and shape.text_frame is not None:
                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            if run.hyperlink and run.hyperlink.address:
                                self.links.append(run.hyperlink.address)

        print(self.links, len(self.links))
        return self.links

    def extract_images(self):
        doc = self.file_loader.loaded_pptx

        for slide_num, slide in enumerate(doc.slides):
            for shape in slide.shapes:
                if shape.shape_type == 13:  # Shape type 13 refers to picture
                    self.images.append(shape.image.blob)

        return self.images, "jpeg"

    def extract_tables(self):
        doc = self.file_loader.loaded_pptx

        for slide_num, slide in enumerate(doc.slides):
            for shape in slide.shapes:
                if hasattr(shape, "table"):
                    table = shape.table
                    table_data = []
                    for row in table.rows:
                        row_data = []
                        for cell in row.cells:
                            row_data.append(cell.text)
                        table_data.append(row_data)
                    self.tables.append(table_data)

        print("ppt table", self.tables)
        return self.tables
