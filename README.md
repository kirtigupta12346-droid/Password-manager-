# 🔐 Secure Password Manager Vault

A full-stack, secure desktop web application built using Python, Streamlit, and SQLite. This application allows users to safely store, generate, and manage their account credentials online using industry-standard cryptographic encryption.

---

## 🚀 Live Demo
You can access the live running model of this project here:  
🔗 **[https://sb4fd4etwtvmhdcryyqmaa.streamlit.app/]** *(Note: Paste your actual streamlit.app link here)*

---

## ✨ Key Features
- **Secure Vault Storage**: Built on a relational local SQLite database engine to permanently store login records without data loss.
- **Fernet Cryptography**: Implements symmetric encryption via the Python `cryptography` library. Passwords are mathematically scrambled before saving to ensure zero-knowledge data security.
- **Automated Password Generator**: Integrates a cryptographically secure random sequence algorithm using Python's `secrets` module to generate high-strength randomized passwords.
- **Modern User Interface**: A minimalist web frontend designed with a responsive sidebar navigation menu for a seamless user experience.
- **Dynamic CRUD Operations**: Users can safely add new credentials, filter search results instantly by website name, and delete obsolete entries with a single click.

---

## 🛡️ Security Architecture
1. **Zero Plain-Text Policy**: No passwords are saved in human-readable plain text inside the database.
2. **Persistent Encryption Key**: A unique encryption key (`secret.key`) is automatically generated on the first boot to handle all continuous encryption and decryption processes locally.

---

## 🛠️ Technology Stack Used
- **Backend Core**: Python 3.x
- **Database Engine**: SQLite3
- **Security & Encryption**: Cryptography Framework (`Fernet`)
- **Web Frontend**: Streamlit Framework

---

## 💻 How to Run Locally

If you wish to test or run this project on your local machine, follow these steps:

### 1. Clone or Download the Project Folder
Ensure all project files (`app.py` and `requirements.txt`) are stored in a single folder.

### 2. Install Required Dependencies
Open your VS Code Terminal or Command Prompt inside the project directory and run:
```bash
pip install -r requirements.txt
```

### 3. Launch the Web Application Server
Execute the framework sequence call in your terminal:
```bash
python -m streamlit run app.py
```
*The app will automatically open in a new tab inside your default web browser at `http://localhost:8501`.*

---

## 📂 Project Structure
```text
Secure-Password-Manager/
│
├── app.py               # Combined Frontend Layout & Backend Execution Script
├── requirements.txt     # Python Library Dependencies List
├── README.md            # Project Documentation & Architecture Overview
├── vault.db             # Local Relational SQLite Database File (Auto-generated)
└── secret.key           # Symmetric Cryptographic Encryption Key File (Auto-generated)
```
