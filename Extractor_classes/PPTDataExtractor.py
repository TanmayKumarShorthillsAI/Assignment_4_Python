from Extractor_classes.DataExtractor import DataExtractor


class PPTDataExtractor(DataExtractor):
    def __init__(self, file_loader):
        super().__init__(file_loader)
        self.file_name = str(file_loader.file_path).split("/")[-1].split(".")[0]
        self.text_metadata = []
        self.image_metadata = []
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

        return self.text

    def extract_links(self):
        doc = self.file_loader.loaded_pptx

        for slide_num, slide in enumerate(doc.slides):
            for shape in slide.shapes:
                if hasattr(shape, "text_frame") and shape.text_frame is not None:
                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            if run.hyperlink and run.hyperlink.address:
                                self.links.append(run.hyperlink.address)
        return self.links

    def extract_images(self):
        doc = self.file_loader.loaded_pptx

        for slide_num, slide in enumerate(doc.slides):
            for shape in slide.shapes:
                if shape.shape_type == 13:  # Shape type 13 refers to picture
                    image = shape.image
                    image_ext = image.ext
                    self.images.append({"blob": image.blob, "format": image_ext})

        return self.images

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

        return self.tables

    def extract_metadata(self):
        doc = self.file_loader.loaded_pptx
        for slide_num, slide in enumerate(doc.slides):
            for shape in slide.shapes:
                # if not hasattr(shape, "has_text_frame") or not shape.has_text_frame:
                #     continue
                if not hasattr(shape, "has_text_frame") or not shape.has_text_frame:
                    continue
                for paragraph in shape.text_frame.paragraphs:
                    # Extract font information from each run (part of the paragraph)
                    for run in paragraph.runs:
                        text = run.text
                        font = run.font
                        font_name = font.name
                        font_size = font.size
                        bold = font.bold
                        italic = font.italic
                        heading = False

                        # Check if the text seems like a heading based on its style (bold, large font, etc.)
                        if bold or (
                            font_size and font_size.pt >= 24
                        ):  # Adjust threshold for heading detection
                            heading = True

                        self.text_metadata.append(
                            {
                                "Text": text,
                                "font_size": font_size,
                                "heading": heading,
                                "font_name": font_name,
                            }
                        )
        # print(self.text_metadata)

        # image metadata
        for slide_num, slide in enumerate(doc.slides):
            for shape in slide.shapes:
                if shape.shape_type == 13:  # Shape type 13 refers to picture
                    image = shape.image

                    self.image_metadata.append(
                        {
                            "file_name": self.file_name,
                            "slide_number": slide_num + 1,
                            "format": image.ext,
                            "resolution": str(image.size[0]) + "x" + str(image.size[1]),
                        }
                    )
        return self.text_metadata, self.image_metadata
