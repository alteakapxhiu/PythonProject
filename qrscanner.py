import qrcode
from flask import Flask, render_template, request
from io import BytesIO
from base64 import b64encode

# Initialize the Flask application
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
