import numpy as np
from PIL import Image
from ultralytics import YOLO
import pytesseract
import PyPDF2
import docx
import re
from filetype import guess
from io import BytesIO


class TextParser:
    regexes = {
        'inn': re.compile(r'[^\d]\d{10,12}[^\d]'),
        'kpp': re.compile(r'[^\d]\d{9}[^\d]'),
        'pay_acc': re.compile(r'[^\d](4\d{19})|(\d{20})[^\d]'),
        'corr_acc': re.compile(r'[^\d]30101\d{15}[^\d]'),
        'bik': re.compile(r'[^\d]04\d{7}[^\d]')
    }

    def __get_data(self, text: str):
        return {k: reg.findall(text)
                for k, reg in self.regexes.items()}

    def pdf(self, file):
        """
        parse pdf file
        """
        reader = PyPDF2.PdfReader(file)
        data = reader.pages[0].extract_text()
        return self.__get_data(data)

    def docx(self, file):
        """
        parse docx file
        """
        docx_bytes = BytesIO(file.read())
        doc = docx.Document(docx_bytes).paragraphs
        docx_bytes.close()
        data = '\n'.join([para.text for para in doc])
        return self.__get_data(data)


class ImageParser:
    def __init__(self, path_to_model: str) -> None:
        self.model = YOLO(path_to_model)
        self.classes = self.model.names
        # print(f"{self.classes=}, {self.model.device=}")

    def __call__(self, file, pad: int = 5):
        """
        :param file: file-like object with open(), close() methods etc.
        :param pad: padding for selected region of interest
        :return: dictionary with 'inn', 'kpp', 'pay_acc', 'cor_acc', 'bik' fields
        """
        image_data = Image.open(file)
        model_results = self.model([image_data])
        storage = {}
        for box in model_results[0].boxes:
            region = box.xyxy.cpu().numpy() + np.array((-pad, -pad, pad, pad))
            cls = self.classes[int(box.cls[0])]
            roi = region.crop(region[0].tolist())
            data = pytesseract.image_to_string(roi)
            storage[cls] = data.strip()
        return storage


class FileParser:
    def __init__(self):
        # self.image_parser = ImageParser('yolov8-1503.pt')
        self.text_parser = TextParser()

    def __call__(self, file):
        filetype = guess(file).mime
        print(file, filetype)
        match filetype:
            case 'image/jpeg' | 'image/png':
                # return {'data': self.image_parser(file)}
                return {'data': 'self.image_parser(file)'}
            case 'application/pdf':
                return {'data': self.text_parser.pdf(file)}
                # return {'data': 'self.text_parser.pdf(file)'}
            case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                return {'data': self.text_parser.docx(file)}
                # return {'data': 'self.text_parser.docx(file)'}
            case _:
                return {'data': []}
