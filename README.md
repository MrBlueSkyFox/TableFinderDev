python 3.9 was used to create exe

run to_exe to create exe file

args to pass
-p path to image that will be used
-o path to output dir where result will be stored(name of file will bi {image_name}.json)
-t path to tesseract exe
-t_cache path to directory for hugging face hub
-ocr_cache path to directory for ocr model
-tr threshold for table detection from 0 to 1


example:
.\table_finder.exe -p C:\Users\tigra\PycharmProjects\OcrResearch\data\fifo_normalize\FIO_1_page-0001.jpg -o C:
\Users\tigra\PycharmProjects\OcrResearch\data\res\res_exe -t "C:\Program Files\Tesseract-OCR\tesseract.exe" -t_cache "C:
\Users\tigra\PycharmProjects\OcrResearch\models" -ocr_cache "C:\Users\tigra\PycharmProjects\OcrResearch\models\easy_ocr"
.\table_finder.exe -p C:\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\tmp4AF4.jpg -o C:
\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\res -t "C:\Program Files\Tesseract-OCR\tesseract.exe" -t_cache "C:
\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\models" -ocr_cache "C:
\Users\t.abraamyan\Documents\PythonPRJ\TableFinderDev\models\easy_ocr"

create dev env for linux bin
docker build -t table-dev-container .
create container (Debian based)
docker run -dit --restart=unless-stopped -v .:/home/app --name table_finder table-dev-container
attach it using
docker exec -it table_finder bash
python to_exe.py

chmod +x dist/table_finder
./table_finder -p /home/app/data/FIO_1/FIO_1_0.jpg \
    -o /home/app/res \
    -t /usr/bin/tesseract \
    -t_cache /home/app/models \
    -ocr_cache /home/app/models/easy_ocr \
    -d True
