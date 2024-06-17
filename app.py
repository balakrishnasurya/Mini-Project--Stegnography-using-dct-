from flask import Flask, render_template, request, redirect, url_for
from decode import decode as decode_function
from encode import encode as encode_function
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

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
            
            # Generate RSA key pair dynamically
            private_key, public_key = generate_rsa_key_pair()
            
            # Encrypt secret message using RSA
            encrypted_secret = encrypt_message(public_key, secret)
            
            # Encode encrypted secret message into image
            encode_function(filepath, encrypted_secret)
            encoded_filepath = os.path.join(app.config['ENCODED_FOLDER'], "dct_" + file.filename)
            
            # Save private key to a file (optional) or return it in the response
            private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')
            
            return f'Encoded image saved at {encoded_filepath}.<br>Private Key (save this securely):<br><textarea readonly>{private_key_pem}</textarea>'
    return render_template("encode.html")

@app.route("/decode", methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        if 'photo' not in request.files or 'private_key' not in request.form:
            return 'No file or private key part'
        file = request.files['photo']
        private_key_pem = request.form['private_key']
        if file.filename == '':
            return 'No selected file'
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Load RSA private key
            private_key = load_private_key(private_key_pem)
            
            # Decode image to get encrypted secret message
            encrypted_secret = decode_function(filepath)
            
            # Decrypt encrypted secret message using RSA
            decrypted_secret = decrypt_message(private_key, encrypted_secret)
            
            return f'Decoded message: {decrypted_secret.decode()}'
    return render_template("decode.html")


def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_message(public_key, message):
    encrypted_message = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message

def decrypt_message(private_key, encrypted_message):
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message

def load_private_key(private_key_pem):
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
        backend=default_backend()
    )
    return private_key

if __name__ == '__main__':
    app.run(debug=True)