import PyInstaller.__main__

PyInstaller.__main__.run([
    'dev_deskew.py',
    "--name=dev_desk",
    '--onefile',
    # '--onedir',
    "-y",
    # "-add-data", "models/;models/",
    # "--add-data=models;models",
    # "--add-binary", "C:\Program Files\ImageMagick-7.1.1-Q16-HDRI:wand",
    # "--collect-submodules", "transformers",
    # "--hidden-import", "numpy",
    # "--copy-metadata", "numpy",
    "--collect-submodules", "transformers",
    # "--hidden-import", "numpy",
    "--collect-data", "torch",
    "--copy-metadata", "torch",
    "--copy-metadata", "numpy",

    # "--collect-data", "torch",
    # "--copy-metadata", "timm"
])

# exutable_entry_poin.exe
# -p C:\Users\tigra\PycharmProjects\OcrResearch\data\fifo_normalize\FIO_1_page-0001.jpg
# -o C:\Users\tigra\PycharmProjects\OcrResearch\data\res\res_exe
# -t "C:\Program Files\Tesseract-OCR\tesseract.exe"
# -t_cache "C:\Users\tigra\PycharmProjects\OcrResearch\models"
# -ocr_cache "C:\Users\tigra\PycharmProjects\OcrResearch\models\easy_ocr"
