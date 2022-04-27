from io import BytesIO
from PIL.Image import register_open
import cv2
import numpy as np
import pytesseract
import traceback
import requests
from PIL import Image
from io import BytesIO
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM


import io

url = "https://api-ipay.vietinbank.vn/api/get-captcha/iK0ZgMQOi"
img_dir = "F:\\OCR\OCR_pictures"
img_dir = 'F:\\OCR\OCR_pictures\"='

def preprocess(img):
    img = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY) # change color image
    thresh, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY) #theshold color of image
    kernel = np.one((2,2), np.uint(8)) # square matrix of ones 2D 2X2
    dilation = cv2.dilate(binary, kernel, iterations=1) # Morphological Dilation of a Binary Image: make path of image darker
    return dilation

def  read(img):
    img_ = preprocess(img)
    
    try:
        text = pytesseract.image_to_string(img_, lang='eng', config="--oem 3 --psm 8") # an opical character recognition: image => text. config???
        text = ''.join([c for c in text if c.isalnum()])
        return text   
    except Exception as e:
        traceback.print_tb(e.__traceback__) # report containing the fuction calls
        print(e)
        return None

def download(n_samples):
    start_id = 0
    for i in range(start_id, n_samples):
    # for i in range(0,1):
        
        headers = {
            'authority': 'api-ipay.vietinbank.vn',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'vi,en;q=0.9',
            'cookie': '_gcl_au=1.1.559116852.1638069881; __utmc=154886719; __utma=154886719.128846460.1638069881.1640002484.1640661450.3; __utmz=154886719.1640661450.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _ga=GA1.1.128846460.1638069881; _ga_QY3N1CT7RM=GS1.1.1640677717.2.0.1640677717.0',   
        }
        
        response = requests.get('https://api-ipay.vietinbank.vn/api/get-captcha/iK0ZgMQOi', headers=headers, verify=False)
        # print(response)
        # print(response.content)

        label = "viettinbank"
        filename = "{:05}_{}.png".format(i, label)

        svg_io = io.StringIO(response.content.decode('utf8'))
        drawing = svg2rlg(svg_io)
        renderPM.drawToFile(drawing, filename, fmt="PNG")


        # # img = Image.open(BytesIO(response.content))

        # img = np.array(img)[:, :, :3]
        # label = "test"
        # filename = "{:05}_{}.png".format(i, label)
        # cv2.imwrite(os.path.join(img_dir, filename), img)

if __name__ == '__main__':
    download(200)