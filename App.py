from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
import base64
import os
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB limit

# Generate encryption key (keep same while server running)
key = Fernet.generate_key()
cipher = Fernet(key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    if 'file' not in request.files:
        return redirect(url_for('home'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('home'))

    filename = secure_filename(file.filename)
    if not filename:
        return redirect(url_for('home'))
    file_data = file.read()

    # Encrypt file data
    encrypted_data = cipher.encrypt(file_data)

    # Combine filename + encrypted data
    package = {
        "filename": filename,
        "data": base64.b64encode(encrypted_data).decode()
    }

    # Convert to JSON → then Base64 encode
    final_code = base64.urlsafe_b64encode(json.dumps(package).encode()).decode()

    return render_template("index.html", secret_code=final_code)

@app.route("/decrypt", methods=["POST"])
def decrypt():
    secret_code = request.form["secret"]

    try:
        # Decode package
        decoded_package = base64.urlsafe_b64decode(secret_code.encode())
        package = json.loads(decoded_package.decode())

        filename = secure_filename(package["filename"])
        if not filename:
            return "Invalid or Corrupted Secure Code"
        encrypted_data = base64.b64decode(package["data"])

        # Decrypt
        decrypted_data = cipher.decrypt(encrypted_data)

        # Restore exact original file
        with open(filename, "wb") as f:
            f.write(decrypted_data)

        return send_file(filename, as_attachment=True)

    except:
        return "Invalid or Corrupted Secure Code"

if __name__ == "__main__":
    app.run(debug=False)
