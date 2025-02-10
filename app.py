from flask import Flask, render_template, request, send_file
import fitz  
import openai
import qrcode
from flask import Flask, render_template, request
from io import BytesIO
from base64 import b64encode
import os
from flask import Flask, render_template, request, url_for
from flask import Flask, request, jsonify, render_template

from gtts import gTTS
import warnings

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")  # Fetch API key securely from environment variable


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

@app.route('/text2speech', methods=['GET', 'POST'])
def text2speech():
    warnings.filterwarnings("default")
    
    if request.method == 'POST':
        text = request.form.get('text', 'Hello')  
        language = 'en'
        
        # Create the gTTS object
        obj = gTTS(text=text, lang=language, slow=False)
        
        # Define the path to save the file inside the 'static' directory
        save_path = os.path.join(app.static_folder, 'sample.mp3')
        
        try:
            # Check if the 'static' folder exists and create it if not
            if not os.path.exists(app.static_folder):
                os.makedirs(app.static_folder)
            
            # Save the audio file
            print(f"Saving file to: {save_path}")
            obj.save(save_path)
            print(f"File saved successfully at {os.path.abspath(save_path)}")
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred during text-to-speech conversion: {e}", 500
        
        if os.path.exists(save_path):
            print("File exists in the directory")
            return render_template('text2speech.html', data=url_for('static', filename='sample.mp3'))

        else:
            print("File does not exist in the directory")
            return "File not found after saving.", 500
    
    return render_template('text2speech.html')

@app.route("/chatbot", methods=["POST"])
def chatbot():
    print("Received request:", request.json)

    user_message = request.json.get("message")
    
    if not user_message:
        print("No message received.")
        return jsonify({"response": "No message received."})

    print(f"User message: '{user_message}'")

    try:
        # OpenAI API call using correct syntax
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use the correct model name (e.g., "gpt-4")
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        # Get bot's response
        bot_response = response['choices'][0]['message']['content']
        print(f"Bot response: '{bot_response}'")

        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Sorry, there was an error processing your message."})


# Route for serving the chatbot UI
@app.route("/chatbot", methods=["GET"])
def chatbot_html():
    return render_template('chatbot.html')


if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)