FROM python:3.9-slim-bullseye

RUN apt-get update && apt-get install -y curl

RUN apt-get install tesseract-ocr imagemagick -y
RUN apt-get install binutils -y
RUN apt-get install tesseract-ocr-rus  -y
COPY req.txt /home/req.txt
RUN pip install -r /home/req.txt
