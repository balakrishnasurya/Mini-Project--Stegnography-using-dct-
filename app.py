from flask import Flask, render_template, request, redirect, url_for
from decode import decode as decode_function
from encode import encode as encode_function
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ENCODED_FOLDER'] = 'Encoded_image'
app.config['DECODED_FOLDER'] = 'Decoded_image'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ENCODED_FOLDER'], exist_ok=True)
os.makedirs(app.config['DECODED_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        if 'photo' not in request.files or 'secret' not in request.form:
            return 'No file or text part'
        file = request.files['photo']
        secret = request.form['secret']
        if file.filename == '':
            return 'No selected file'
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            encoded_filepath = encode_function(filepath, secret)
            return f'Encoded image saved at {encoded_filepath}'
    return render_template("encode.html")

@app.route("/decode", methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        if 'photo' not in request.files:
            return 'No file part'
        file = request.files['photo']
        if file.filename == '':
            return 'No selected file'
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            hidden_text = decode_function(filepath)
            return f'Hidden message: {hidden_text}'
    return render_template("decode.html")

if __name__ == '__main__':
    app.run(debug=True)
