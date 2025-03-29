from flask import Flask, render_template, request, send_file
import fitz  
from google import genai
import qrcode
from flask import Flask, render_template, request
from io import BytesIO
from base64 import b64encode
import os
from flask import Flask, render_template, request, url_for
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from gtts import gTTS
import warnings
import speech_recognition as sr
import pyttsx3

app = Flask(__name__)
load_dotenv()  # Load environment variables from the .env file

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


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


# Function to generate voice from text
def generate_voice(text):
    tts = gTTS(text=text, lang="en", slow=False)
    voice_path = os.path.join(app.static_folder, "response.mp3")
    
    if not os.path.exists(app.static_folder):
        os.makedirs(app.static_folder)

    tts.save(voice_path)
    return url_for('static', filename="response.mp3")

# Function to process speech input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Could not process voice input."
        
# Voice Chatbot Route (Speech Input and Output)
@app.route("/voicechat", methods=["POST"])
def voicechat():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)  # Convert speech to text
            print(f"Recognized: {text}")

            return jsonify({"response": text})  # Send text back to frontend
        except sr.UnknownValueError:
            return jsonify({"response": "Sorry, I couldn't understand that."})
        except sr.RequestError as e:
            return jsonify({"response": f"Error connecting to speech service: {e}"}), 500


@app.route("/chatbot", methods=["POST"])
def chatbot():
    print("Received request:", request.json)

    user_message = request.json.get("message")

    if not user_message:
        print("No message received.")
        return jsonify({"response": "No message received."})

    print(f"User message: '{user_message}'")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",  
            contents=user_message  
        )
        bot_response = response.text
        print(f"Bot response: '{bot_response}'")

        return jsonify({"response": bot_response})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Sorry, there was an error processing your message."}), 500

@app.route("/chatbot", methods=["GET"])
def chatbot_html():
    return render_template('chatbot.html')

if __name__ == "__main__":
    app.run(debug=True)