# pip install flask
import os  
from flask import Flask, render_template, request
import cv2
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image

# import our OCR function
# from ocr_core import ocr_core
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def ocr_core(filename):  
    """This function will handle the core OCR processing of images"""
    text = pytesseract.image_to_string(Image.open(filename))  
    # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

# define a folder to store and later serve the images
UPLOAD_FOLDER = 'static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

# function to check the file extension
def allowed_file(filename):  
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page
@app.route('/')  # localhost:5000
def home_page():  
    return render_template('index.html')


@app.route('/demo')  # localhost:5000
def demo_page():  
    return render_template('demo.html')


# {% Python_syntax %}
# {{ data }}
# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():  
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):  
            # if file is uploaded and its extension is .jpg, .png or .jpeg
            # call the OCR function on it
            extracted_text = ocr_core(file)

            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':  
    app.run()

# Start the server - python app.py
# Stop the server - Ctrl + c