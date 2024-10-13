from Extractor_classes.DataExtractor import DataExtractor

# import fitz
import pandas as pd
import tabula


class PDFDataExtractor(DataExtractor):
    def __init__(self, file_loader):
        super().__init__(file_loader)
        self.file_name = str(file_loader.loaded_pdf).split("/")[-1].split(".")[0]
        self.text = []
        self.images = []
        self.links = []
        self.tables = []

    # Extract text from pdf
    def extract_text(self):
        doc = self.file_loader.loaded_pdf

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)

            self.text.append(page.get_text("text"))
        return self.text, self.file_name

    # Extract images from pdf
    def extract_images(self):
        doc = self.file_loader.loaded_pdf

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            images = page.get_images(full=True)

            # Extract and process each image
            for img_index, img in enumerate(images):
                xref = img[0]  # XREF of the image
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                self.images.append(image_bytes)

        return self.images, image_ext

    # Extract links from pdf
    def extract_links(self):
        doc = self.file_loader.loaded_pdf

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)

            for link in page.get_links():
                if "uri" in link:
                    self.links.append(link["uri"])

        return self.links

    # Extract tables from pdf
    def extract_tables(self):
        doc_path = self.file_loader.file_path

        temp_tables = tabula.read_pdf(doc_path, pages="all", multiple_tables=True)
        for x in temp_tables:
            arr = [x.columns.tolist()] + x.values.tolist()
            self.tables.append(arr)

        return self.tables
