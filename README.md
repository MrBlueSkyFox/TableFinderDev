python 3.9 was used to create exe

run to_exe to create exe file

args to pass
-p  path to image that will be used
-o path to output dir where result will be stored(name of file will bi {image_name}.json)
-t path to tesseract exe
-t_cache path to directory for hugging face hub 
-ocr_cache path to directory for ocr model

example:
.\table_finder.exe -p C:\Users\tigra\PycharmProjects\OcrResearch\data\fifo_normalize\FIO_1_page-0001.jpg -o C:\Users\tigra\PycharmProjects\OcrResearch\data\res\res_exe -t "C:\Program Files\Tesseract-OCR\tesseract.exe" -t_cache "C:\Users\tigra\PycharmProjects\OcrResearch\models" -ocr_cache "C:\Users\tigra\PycharmProjects\OcrResearch\models\easy_ocr"