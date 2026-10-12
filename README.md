# Secure File Encryption Web Application

A small Flask web application that encrypts an uploaded file and creates a shareable encoded code. The receiver pastes the code into the decryption section to restore and download the original file.

## Technologies
- Python
- Flask
- Fernet (`cryptography`)
- HTML, CSS, JavaScript
- Base64 and JSON

## Features
- Upload files up to 1 MB
- Encrypt file contents using Fernet symmetric encryption
- Package the original filename with the encrypted data
- Generate a copyable secure code
- Decode and decrypt the code to download the original file

## Project structure
```text
Secure-File-Encryption/
├── App.py
├── templates/
│   └── index.html
├── requirements.txt
└── README.md
```

## Run locally
1. Install Python 3.
2. Open a terminal in this project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   python App.py
   ```
5. Open the local URL shown in the terminal (usually `http://127.0.0.1:5000`).

## Important limitations
- The Fernet key is generated when the server starts and is kept in memory. Codes created before a server restart cannot be decrypted after the restart. A receiver using another server instance also will not have the same key.
- This is an academic/demo project, not a production-ready file-sharing service. Do not use it for sensitive real-world files without implementing persistent, secure key management and other deployment security controls.
- Base64 is encoding, not encryption. Fernet provides the encryption.
