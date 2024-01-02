import os
from pathlib import Path
from util import get_all_pdf_files_in_directory
import pdf2image

poppler_path = r"D:\Programms\poppler-23.11.0\Library\bin"


def convert_pdf_to_images(directory: str):
    pdf_files_path = get_all_pdf_files_in_directory(directory)
    for pdf_path in pdf_files_path:
        with open(pdf_path, "rb") as f:
            pdf = pdf2image.convert_from_bytes(f.read(), poppler_path=poppler_path)
            file_name = os.path.splitext(os.path.basename(pdf_path))[0]
            dir_to_save = os.path.join(
                os.path.dirname(pdf_path),
                file_name
            )
            print(f"Start processing file {pdf_path}")
            Path(dir_to_save).mkdir(parents=True, exist_ok=True)
            for idx, pdf_img in enumerate(pdf):
                save_name = os.path.join(dir_to_save, f"{file_name}_{idx}.jpg")
                pdf_img.save(save_name)
            print(f"End processing file {pdf_path} img in file: {len(pdf)}")


if __name__ == "__main__":
    convert_pdf_to_images("data")
