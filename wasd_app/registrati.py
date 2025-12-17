import sqlite3
import hashlib
import os
import binascii
import getpass

DB_NAME = "alphaBotDB.db"
ITERATIONS = 200_000


def init_db():
    """Crea database e tabella se non esistono"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        ITERATIONS
    )
    return f"pbkdf2_sha256${ITERATIONS}$" + binascii.hexlify(salt + key).decode()


def register_user():
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    confirm = getpass.getpass("Conferma password: ")

    if not username or not password:
        print("Username e password obbligatori")
        return

    if password != confirm:
        print("Le password non coincidono")
        return

    password_hash = hash_password(password)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        """, (username, password_hash))

        conn.commit()
        print("Registrazione completata")

    except sqlite3.IntegrityError:
        print("Username già esistente")

    except Exception as e:
        print("Errore:", e)

    finally:
        conn.close()


if __name__ == "__main__":
    init_db()       
    register_user()  
