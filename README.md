python 3.9 was used to create exe

run to_exe to create exe file

args to pass
-p  path to image that will be used
-o path to output dir where result will be stored(name of file will bi {image_name}.json)
-t path to tesseract exe
-t_cache path to directory for hugging face hub 
-ocr_cache path to directory for ocr model
-tr threshold for table detection from 0 to 1


example:
.\table_finder.exe -p C:\Users\tigra\PycharmProjects\OcrResearch\data\fifo_normalize\FIO_1_page-0001.jpg -o C:\Users\tigra\PycharmProjects\OcrResearch\data\res\res_exe -t "C:\Program Files\Tesseract-OCR\tesseract.exe" -t_cache "C:\Users\tigra\PycharmProjects\OcrResearch\models" -ocr_cache "C:\Users\tigra\PycharmProjects\OcrResearch\models\easy_ocr"
.\table_finder.exe -p C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\tmp4AF4.jpg -o C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\res -t "C:\Program Files\Tesseract-OCR\tesseract.exe" -t_cache "C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\models" -ocr_cache "C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\models\easy_ocr"