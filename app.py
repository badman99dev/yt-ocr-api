from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import os
import tempfile

app = Flask(__name__)
CORS(app)  # CORS always ON

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ocr', methods=['POST'])
def ocr_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, file.filename)
        file.save(file_path)

        text = ""

        try:
            if file.filename.lower().endswith(".pdf"):
                pdf_doc = fitz.open(file_path)
                for i, page in enumerate(pdf_doc):
                    pix = page.get_pixmap(dpi=300)
                    img_path = os.path.join(tmpdir, f"page_{i}.png")
                    pix.save(img_path)
                    text += pytesseract.image_to_string(Image.open(img_path), lang="hin+eng") + "\n"
            else:
                text = pytesseract.image_to_string(Image.open(file_path), lang="hin+eng")
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'text': text.strip()})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
