from flask import Flask, render_template, request, send_file
import fitz  
import qrcode
from flask import Flask, render_template, request
from io import BytesIO
from base64 import b64encode
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        memory = BytesIO()
        data = request.form.get('link')
        img = qrcode.make(data)
        img.save(memory)
        memory.seek(0)
        base64_img = "data:image/png;base64," + b64encode(memory.getvalue()).decode('ascii')
        return render_template('index.html', data=base64_img)
    else:
        return render_template('index.html', data=None)

@app.route('/pdftojpg', methods=['GET', 'POST'])
def pdftojpg():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return "Ska asnje dokument", 400

        pdf_file = request.files['pdf_file']
        if pdf_file.filename == '':
            return "Asnje dokument i zgjedhur", 400

        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
        pdf_file.save(pdf_path)

        try:
            pdf_document = fitz.open(pdf_path)
            page = pdf_document.load_page(0)  
            pix = page.get_pixmap()
            output_file = pdf_path.replace('.pdf', '-page-1.jpg')
            pix.save(output_file)
            pdf_document.close()

            if os.path.exists(output_file):
                print(f"File ready for download: {output_file}")
            else:
                print(f"Error: File not found: {output_file}")

            return send_file(output_file, as_attachment=True)
        except Exception as e:
            return f"An error occurred: {e}", 500
        finally:
            os.remove(pdf_path)

    return render_template('pdftojpg.html')

@app.route('/pdftojpeg', methods=['GET', 'POST'])
def pdftojpeg():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return "Ska asnje dokument", 400

        pdf_file = request.files['pdf_file']
        if pdf_file.filename == '':
            return "Asnje dokument i zgjedhur", 400

        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
        pdf_file.save(pdf_path)

        try:
            pdf_document = fitz.open(pdf_path)
            page = pdf_document.load_page(0)  
            pix = page.get_pixmap()
            output_file = pdf_path.replace('.pdf', '-page-1.jpeg')
            pix.save(output_file)
            pdf_document.close()

            if os.path.exists(output_file):
                print(f"File ready for download: {output_file}")
            else:
                print(f"Error: File not found: {output_file}")

            return send_file(output_file, as_attachment=True)
        except Exception as e:
            return f"An error occurred: {e}", 500
        finally:
            os.remove(pdf_path)

    return render_template('pdftojpeg.html')


@app.route('/pdftopng', methods=['GET', 'POST'])
def pdftopng():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return "Ska asnje dokument", 400

        pdf_file = request.files['pdf_file']
        if pdf_file.filename == '':
            return "Asnje dokument i zgjedhur", 400

        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
        pdf_file.save(pdf_path)

        try:
            pdf_document = fitz.open(pdf_path)
            page = pdf_document.load_page(0)  
            pix = page.get_pixmap()
            output_file = pdf_path.replace('.pdf', '-page-1.png')
            pix.save(output_file)
            pdf_document.close()

            if os.path.exists(output_file):
                print(f"File ready for download: {output_file}")
            else:
                print(f"Error: File not found: {output_file}")

            return send_file(output_file, as_attachment=True)
        except Exception as e:
            return f"An error occurred: {e}", 500
        finally:
            os.remove(pdf_path)

    return render_template('pdftopng.html')


if __name__ == "__main__":
    app.run(debug=True)
