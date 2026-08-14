import streamlit as st
import sqlite3
import secrets
import string
import os
from cryptography.fernet import Fernet

# ==============================================================================
# ⚙️ BLOCK A: BACKEND ARCHITECTURE (Database & Cryptography Engine)
# ==============================================================================

DB_FILE = "vault.db"
KEY_FILE = "secret.key"

def load_or_create_key():
    """Generates or loads a persistent encryption key file."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key

# Initialize cryptographic engine parameters
SECRET_KEY = load_or_create_key()
cipher = Fernet(SECRET_KEY)

def encrypt_data(plain_text: str) -> str:
    """Backend cipher mechanism to secure password blocks."""
    return cipher.encrypt(plain_text.encode()).decode()

def decrypt_data(cipher_text: str) -> str:
    """Backend logic to translate secure hash variables back to original form."""
    try:
        return cipher.decrypt(cipher_text.encode()).decode()
    except Exception:
        return "⚠️ Decryption Error!"

def setup_database():
    """Builds structural SQL tables inside your vault environment."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

def generate_strong_password(length=16) -> str:
    """Randomized sequence string logic algorithm."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

# Boot database connectivity parameters automatically
setup_database()


# ==============================================================================
# 🎨 BLOCK B: FRONTEND APPLICATION LAYOUT (Streamlit Rendering Interface)
# ==============================================================================

st.set_page_config(page_title="Secure Password Vault", page_icon="🔐", layout="centered")

st.title("🔐 Secure Password Manager Vault")
st.markdown("---")

# Navigation Panel Dashboard Menu Selector
menu_choice = st.sidebar.radio(
    "Navigation Menu",
    ["➕ Add New Password", "🔍 View & Manage Vault"]
)

# ---- FRONTEND VIEW 1: SAVE INTERFACE ----
if menu_choice == "➕ Add New Password":
    st.subheader("Add New Account Credentials")
    
    with st.form("add_form", clear_on_submit=True):
        web_input = st.text_input("Website Name", placeholder="e.g., Google, Facebook")
        user_input = st.text_input("Username / Email", placeholder="e.g., user@example.com")
        pass_input = st.text_input("Password", type="password", help="Type your password or generate one below")
        submit_btn = st.form_submit_button("💾 Save Credentials")
    
    st.markdown("### Need a Strong Password?")
    if st.button("🎲 Auto-Generate Random Password"):
        generated_pass = generate_strong_password()
        st.code(generated_pass, language="text")
        st.info("💡 Copy the generated value above and paste it into the Password field.")

    if submit_btn:
        if not web_input or not user_input or not pass_input:
            st.error("❌ Error: All fields are required to process entry data.")
        else:
            encrypted_password = encrypt_data(pass_input)
            
            db = sqlite3.connect(DB_FILE)
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO vault (website, username, encrypted_password) VALUES (?, ?, ?)",
                (web_input.strip().lower(), user_input.strip(), encrypted_password)
            )
            db.commit()
            db.close()
            st.success(f"✅ Success! Your credentials for **{web_input}** have been safely encoded.")

# ---- FRONTEND VIEW 2: SEARCH & ERASE RECORDS ----
elif menu_choice == "🔍 View & Manage Vault":
    st.subheader("Manage Saved Vault Records")
    
    search_query = st.text_input("Search System by Website Name", placeholder="Leave blank to show all accounts").strip().lower()
    
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    
    if search_query:
        cursor.execute("SELECT website, username, encrypted_password FROM vault WHERE website LIKE ?", (f"%{search_query}%",))
    else:
        cursor.execute("SELECT website, username, encrypted_password FROM vault")
        
    records = cursor.fetchall()
    db.close()
    
    if not records:
        st.info("ℹ️ No credential blocks matching your tracking query are found.")
    else:
        st.markdown("### Saved Credentials")
        
        for row in records:
            website_name, username, crypto_pass = row
            real_password = decrypt_data(crypto_pass)
            
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**🌐 Website:** {website_name.capitalize()}")
                    st.markdown(f"**👤 Username:** `{username}`")
                    st.markdown(f"**🔑 Decrypted Password:** `{real_password}`")
                
                with col2:
                    if st.button("🗑️ Delete", key=f"del_{website_name}_{username}"):
                        db = sqlite3.connect(DB_FILE)
                        cursor = db.cursor()
                        cursor.execute("DELETE FROM vault WHERE website = ? AND username = ?", (website_name, username))
                        db.commit()
                        db.close()
                        st.warning(f"Removed system indices context for {website_name.capitalize()}.")
                        st.rerun()