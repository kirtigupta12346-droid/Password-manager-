#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Cell 1: Package Installation
get_ipython().system('pip install cryptography ipywidgets')


# In[2]:


# Cell 2: Database Setup
import sqlite3

def setup_database():
    # Connects to the local database file (creates it if it doesn't exist)
    connection = sqlite3.connect("vault.db")
    cursor = connection.cursor()

    # Create the table to store credentials securely
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
    print("✅ Database created and connected successfully!")

setup_database()


# In[3]:


# Cell 3: Cryptography and Password Generation Engine
import secrets
import string
from cryptography.fernet import Fernet

# Generate a unique encryption key for this notebook session
if 'secret_key' not in globals():
    secret_key = Fernet.generate_key()

cipher = Fernet(secret_key)

# Function to encrypt plain text passwords into a secure cipher text
def encrypt_data(plain_text):
    return cipher.encrypt(plain_text.encode()).decode()

# Function to safely decrypt the cipher text back into plain text
def decrypt_data(cipher_text):
    try:
        return cipher.decrypt(cipher_text.encode()).decode()
    except Exception:
        return "⚠️ Decryption Error!"

# Function to automatically generate highly randomized, strong passwords
def generate_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

print("🔐 Encryption system and password generator are ready!")


# In[4]:


# Cell 4: Interactive Dashboard Interface Layout & Button Logic
import sqlite3
import ipywidgets as widgets
from IPython.display import display, clear_output

# ---- TAB 1: ADD NEW PASSWORDS ----
web_box = widgets.Text(description="Website:")
user_box = widgets.Text(description="Username:")
pass_box = widgets.Text(description="Password:", password=True)
btn_gen = widgets.Button(description="🎲 Generate", button_style='info')
btn_save = widgets.Button(description="💾 Save to Vault", button_style='success')
save_output = widgets.Output()

# ---- TAB 2: VIEW & DELETE PASSWORDS ----
search_box = widgets.Text(description="Search Web:")
btn_search = widgets.Button(description="🔍 Search", button_style='primary')
btn_delete = widgets.Button(description="🗑️ Delete Account", button_style='danger')
search_output = widgets.Output()

# ---- INTERFACE OPERATION LOGIC ----

# Logic for the "Generate" button
def click_generate(b):
    pass_box.value = generate_password()

btn_gen.on_click(click_generate)

# Logic for the "Save to Vault" button
def click_save(b):
    with save_output:
        clear_output()
        if not web_box.value or not user_box.value or not pass_box.value:
            print("❌ Error: All fields are required!")
            return

        # Scramble the password using Cell 3 encryption engine
        encrypted_str = encrypt_data(pass_box.value)

        db = sqlite3.connect("vault.db")
        cursor = db.cursor()
        cursor.execute("INSERT INTO vault (website, username, encrypted_password) VALUES (?, ?, ?)",
                       (web_box.value.strip().lower(), user_box.value.strip(), encrypted_str))
        db.commit()
        db.close()

        print(f"✅ Securely saved credentials for {web_box.value}!")
        web_box.value, user_box.value, pass_box.value = '', '', ''

btn_save.on_click(click_save)

# Logic for the "Search" button
def click_search(b):
    with search_output:
        clear_output()
        db = sqlite3.connect("vault.db")
        cursor = db.cursor()
        cursor.execute("SELECT website, username, encrypted_password FROM vault WHERE website LIKE ?", 
                       (f"%{search_box.value.strip().lower()}%",))
        records = cursor.fetchall()
        db.close()

        if not records:
            print("ℹ️ No matching records found.")
            return

        # Display results on the screen nicely formatted
        print(f"{'Website':<20} | {'Username':<20} | {'Password':<20}")
        print("-" * 65)
        for row in records:
            real_password = decrypt_data(row[2])
            print(f"{row[0]:<20} | {row[1]:<20} | {real_password:<20}")

btn_search.on_click(click_search)

# Logic for the "Delete Account" button
def click_delete(b):
    with search_output:
        clear_output()
        target_web = search_box.value.strip().lower()

        if not target_web:
            print("❌ Error: Please type the exact website name you want to delete into the search box first!")
            return

        db = sqlite3.connect("vault.db")
        cursor = db.cursor()

        # Pre-check: Verify if the website exists in the database before deleting
        cursor.execute("SELECT * FROM vault WHERE website = ?", (target_web,))
        if not cursor.fetchone():
            print(f"ℹ️ No credentials found for '{target_web}' to delete.")
            db.close()
            return

        # SQL Command to wipe out the account row
        cursor.execute("DELETE FROM vault WHERE website = ?", (target_web,))
        db.commit()
        db.close()

        print(f"🗑️ Successfully deleted all saved credentials for '{target_web}'!")
        search_box.value = ''

btn_delete.on_click(click_delete)

# ---- CONSTRUCT RENDERING LAYOUT ----
layout_tab1 = widgets.VBox([web_box, user_box, widgets.HBox([pass_box, btn_gen]), btn_save, save_output])
layout_tab2 = widgets.VBox([widgets.HBox([search_box, btn_search, btn_delete]), search_output])

menu = widgets.Tab()
menu.children = [layout_tab1, layout_tab2]
menu.set_title(0, 'Add New Password')
menu.set_title(1, 'View & Delete Passwords')

# Render layout inside Jupyter
display(menu)


# In[ ]:




