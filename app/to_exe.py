import PyInstaller.__main__
from sys import platform

if platform == "win32":
    image_magic_path = r"D:\Programms\ImageMagick-7.1.1-Q16-HDRI:wand"
else:
    image_magic_path = "/usr/bin/convert:wand/convert"  # not sure if this works
PyInstaller.__main__.run([
    'cli.py',
    "--name=table_finder",
    '--onefile',

    # '--onedir',
    "-y",
    # "-add-data", "models/;models/",
    # "--add-data=models;models",
    "--collect-submodules", "transformers",
    # "--hidden-import", "numpy",
    "--collect-data", "torch",
    "--collect-data", "pytesseract",
    "--collect-data", "pandas",
    "--collect-data", "tqdm",
    "--collect-data", "timm",
    "--copy-metadata", "torch",
    "--copy-metadata", "tqdm",
    "--copy-metadata", "regex",
    "--copy-metadata", "requests",
    "--copy-metadata", "packaging",
    "--copy-metadata", "filelock",
    "--copy-metadata", "numpy",
    "--copy-metadata", "huggingface-hub",
    "--copy-metadata", "safetensors",
    "--copy-metadata", "pyyaml",
    "--copy-metadata", "pytesseract",
    "--copy-metadata", "timm",
    # "--exclude-module", "torch\test",

    "--add-binary", image_magic_path,
    "--exclude-module", "tkinter",

])

# exutable_entry_poin.exe
# -p C:\Users\tigra\PycharmProjects\OcrResearch\data\fifo_normalize\FIO_1_page-0001.jpg
# -o C:\Users\tigra\PycharmProjects\OcrResearch\data\res\res_exe
# -t "C:\Program Files\Tesseract-OCR\tesseract.exe"
# -t_cache "C:\Users\tigra\PycharmProjects\OcrResearch\models"
# -ocr_cache "C:\Users\tigra\PycharmProjects\OcrResearch\models\easy_ocr"
