import PyInstaller.__main__

PyInstaller.__main__.run([
    'executable_entry_point.py',
    "--name=table_finder",
    '--onefile',

    # '--onedir',
    "-y",
    # "-add-data", "models/;models/",
    # "--add-data=models;models",
    "--collect-submodules", "transformers",
    "--hidden-import", "numpy",
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

    "--add-binary", "C:\Program Files\ImageMagick-7.1.1-Q16-HDRI:wand",

])

# exutable_entry_poin.exe
# -p C:\Users\tigra\PycharmProjects\OcrResearch\data\fifo_normalize\FIO_1_page-0001.jpg
# -o C:\Users\tigra\PycharmProjects\OcrResearch\data\res\res_exe
# -t "C:\Program Files\Tesseract-OCR\tesseract.exe"
# -t_cache "C:\Users\tigra\PycharmProjects\OcrResearch\models"
# -ocr_cache "C:\Users\tigra\PycharmProjects\OcrResearch\models\easy_ocr"
