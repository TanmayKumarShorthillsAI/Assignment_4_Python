from DataExtractor import DataExtractor

# import fitz
import tabula


class PDFDataExtractor(DataExtractor):
    def __init__(self, file_loader):
        super().__init__(file_loader)
        self.text = []
        self.images = []
        self.links = []
        self.tables = []

    # Extract text from pdf
    def extract_text(self):
        # self.text = []
        doc = self.file_loader.loaded_pdf

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)

            # Extract text
            self.text.append(page.get_text("text"))
            # with open(f"page_{page_num + 1}_text.txt", "w", encoding="utf-8") as f:
            #     f.write(text)
        # doc.close()
        return super().extract_text()

    # Extract images from pdf
    def extract_images(self):
        doc = self.file_loader.loaded_pdf

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            self.images = page.get_images(full=True)

        print(self.images)

        return super().extract_images()
        # doc.close()

    # Extract links from pdf
    def extract_links(self):
        doc = self.file_loader.loaded_pdf

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            links = []

            for link in page.get_links():
                if "uri" in link:
                    links.append(link["uri"])

            self.links.append(links)

        return super().extract_links()

        # print(self.links[0])

    # Extract tables from pdf
    def extract_tables(self):
        doc_path = self.file_loader.file_path

        self.tables = tabula.read_pdf(doc_path, pages="all", multiple_tables=True)
        print(self.tables)

        return super().extract_tables()
