from Extractor_classes.DataExtractor import DataExtractor
import pandas as pd
import tabula


class PDFDataExtractor(DataExtractor):
    def __init__(self, file_loader):
        super().__init__(file_loader)
        self.doc = self.file_loader.loaded_pdf

    # Extract text from pdf
    def extract_text(self):
        for page_num in range(self.doc.page_count):
            page = self.doc.load_page(page_num)

            self.text.append(page.get_text("text"))
        return self.text

    # Extract images from pdf
    def extract_images(self):
        for page_num in range(self.doc.page_count):
            page = self.doc.load_page(page_num)
            images = page.get_images(full=True)

            # Extract and process each image
            for img_index, img in enumerate(images):
                xref = img[0]  # XREF of the image
                base_image = self.doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                self.images.append(
                    {
                        "file_name": self.file_name,
                        "blob": image_bytes,
                        "format": image_ext,
                    }
                )

        return self.images

    # Extract links from pdf
    def extract_links(self):
        for page_num in range(self.doc.page_count):
            page = self.doc.load_page(page_num)

            for link in page.get_links():
                # print(link)
                if "uri" in link:
                    self.links.append(
                        {"file_name": self.file_name, "link": link["uri"]}
                    )

        return self.links

    # Extract tables from pdf
    def extract_tables(self):
        temp_tables = tabula.read_pdf(
            self.file_loader.file_path, pages="all", multiple_tables=True
        )
        for x in temp_tables:
            arr = [x.columns.tolist()] + x.values.tolist()
            self.tables.append(arr)

        return self.tables

    def extract_metadata(self):
        # store text metadata
        heading_font_size_threshold = 16

        for page_num in range(self.doc.page_count):
            page = self.doc.load_page(page_num)
            text_dict = page.get_text("dict")

            for block in text_dict["blocks"]:
                if "lines" in block:  #
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"]
                            font = span["font"]
                            size = span["size"]
                            is_heading = size > heading_font_size_threshold

                            # Store the metadata as a dictionary for each span of text
                            span_metadata = {
                                "page_number": page_num + 1,
                                "text": text,
                                "font": font,
                                "heading": is_heading,
                            }

                            self.text_metadata.append(span_metadata)

        # store image metadata
        for page_num in range(self.doc.page_count):
            page = self.doc.load_page(page_num)
            images = page.get_images(full=True)

            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = self.doc.extract_image(xref)
                image_ext = base_image["ext"]
                image_width = base_image["width"]
                image_height = base_image["height"]
                resolution = str(image_height) + "x" + str(image_width)

                self.image_metadata.append(
                    {
                        "file_name": self.file_name,
                        "page_number": page_num,
                        "resolution": resolution,
                        "format": image_ext,
                    }
                )
        return self.text_metadata, self.image_metadata
