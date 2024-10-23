# Assignment_4_Python

## Extract Text, Links, Images, and Tables from PDF, DOCX, and PPT with Metadata

### File Structure:

```
├── Extractor_classes
│   ├── DOCXDataExtractor.py
│   ├── DataExtractor.py
│   ├── PDFDataExtractor.py
│   ├── PPTDataExtractor.py
├── Loader_classes
│   ├── DOCXloader.py
│   ├── FileLoader.py
│   ├── PDFloader.py
│   ├── PPTloader.py
│   └── testing
│       ├── test_DOCXloader.py
│       ├── test_PDFloader.py
│       └── test_PPTloader.py
├── README.md
├── Output
├── Sample_files
├── Storage_classes
│   ├── FileStorage.py
│   ├── SQLStorage.py
│   ├── Storage.py
├── main_script.py
```

### Requirements:

- Python version 3.10.x
- pip

```
mysql-connector-python
numpy
pandas
pillow
PyMuPDF
python-docx
python-pptx
tabula-py
```

### Install the requirements:

```bash
pip3 install mysql-connector-python numpy pandas pillow PyMuPDF python-docx python-pptx tabula-py
```

### Features:

#### **For each file format in (.pdf, .pptx and .docx)**

- **Text Extraction**: Extract text and its metadata(text font and headings)
- **Image Extraction**: Extract image and its metadata(imgae extension, page number and image resolution)
- **Link Extraction**: Extract hyperlinks present in the files.
- **Table Extracttion**: Extract tables present in the files in .csv format.
- **Storage of extracted data**: Storage of all of the above mentioned data into directories and SQL database.

### Loader classes:

- FileLoader class is an abstarct class which provides defination for loading file into memory
- Classes : PDFLoader, DOCXLoader, PPTLoader are concrete class which implements the logic for loading the respective files.
- Following libraries are used to load the respective files:
- pdf: PyMuPDF (import fitz then use fitz.open(file_path) to load the pdf)
- docx: python-docx (import docx then use docx.Document(file_path) to load the docx file)
- pptx- python-pptx (import pptx then use pptx.Document(file_path) to load the pptx file)
- Loader_classes folder contains the testing folder with contains the test cases tested.

### Extarctor classes:

- Following the same structure as above DataExtarctor class is an abstract class which provides defination for methods such as extract text, links, images and tables.
- Clsases: PDFDataExtarctor, DOCXDataExtarctor and PPTDataExtarctorare concrete calsses that implement the abstract methods named in the abstarct class DataExatrctor.
- For table extraction in pdf files tabula-py library is used.
- The extracted data is stored in lists (images as blobs) and returned.

### Storage classes:

- Agian the same structure follows in Storage classes, Storage is the abstract class with the abstract method - save.
- FileStorage and SQLStorage are the conctrete classes that inherit Storage class.
- File storage class implements the universal logic to store the extracted data in directory named "output".
- Text and hyperlinks are stored as .txt files and tables as csv files and images as jepg or png.
- The sql storage has database named file_extracted_data which contains three tables : pdf_data, docx_data and pptx_data.
- These tables have the following fields: S.no, file_name, data_type(i.e. text, image, hyperlinks and tables) and extracted_data.

### Usage

- Install the dependencies mentions above adn set your environment variables.
- Run the `main_script.py` file in terminal and provide the file path as input.
