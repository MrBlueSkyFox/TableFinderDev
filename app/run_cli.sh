#!/bin/sh

# Capture the output of "which tesseract" and store it in the TESSERACT_PATH variable
TESSERACT_PATH=$(which tesseract)


python cli.py -p "data/FIO_1/FIO_1_0.jpg"\
    -o "res/FIO_1" \
    -t $TESSERACT_PATH \
    -t_cache "models" \
    -ocr_cache "models/easy_ocr"



