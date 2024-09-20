import tkinter as tk
from tkinter import filedialog, messagebox

class CipherApp:
    def __init__(self, master):
        self.master = master
        master.title("Tugas Kriptografi")
        
        self.text_input = tk.Text(master, height=10, width=50)
        self.text_input.pack(pady=10)

        self.key_entry = tk.Entry(master, width=50)
        self.key_entry.pack(pady=5)
        self.key_entry.insert(0, "Masukkan sandi (min 12)")

        self.upload_button = tk.Button(master, text="Unggah File", command=self.upload_file)
        self.upload_button.pack(pady=5)
        
        self.encrypt_button = tk.Button(master, text="Enkripsi", command=self.encrypt)
        self.encrypt_button.pack(pady=5)
        
        self.decrypt_button = tk.Button(master, text="Deskripsi", command=self.decrypt)
        self.decrypt_button.pack(pady=5)

        self.cipher_choice = tk.StringVar(value="Vigenere")
        self.vigenere_radio = tk.Radiobutton(master, text="Vigenere Cipher", variable=self.cipher_choice, value="Vigenere")
        self.playfair_radio = tk.Radiobutton(master, text="Playfair Cipher", variable=self.cipher_choice, value="Playfair")
        self.hill_radio = tk.Radiobutton(master, text="Hill Cipher", variable=self.cipher_choice, value="Hill")
        
        self.vigenere_radio.pack()
        self.playfair_radio.pack()
        self.hill_radio.pack()

        # Area untuk hasil enkripsi
        self.result_encrypt = tk.Text(master, height=10, width=50, bg="lightgreen")
        self.result_encrypt.pack(pady=10)
        self.result_encrypt.insert(tk.END, "Hasil Enkripsi :\n")

        # Area untuk hasil dekripsi
        self.result_decrypt = tk.Text(master, height=10, width=50, bg="lightyellow")
        self.result_decrypt.pack(pady=10)
        self.result_decrypt.insert(tk.END, "Hasil Deskripsi:\n")

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_input.delete(1.0, tk.END)
                self.text_input.insert(tk.END, content)

    def get_message(self):
        return self.text_input.get(1.0, tk.END).strip()

    def get_key(self):
        key = self.key_entry.get().strip()
        if len(key) < 12:
            messagebox.showerror("Error", "Sandi minimal harus 12 karakter.")
            return None
        return key

    def encrypt(self):
        key = self.get_key()
        if key is None:
            return
        message = self.get_message()
        if self.cipher_choice.get() == "Vigenere":
            result = self.vigenere_encrypt(message, key)
        elif self.cipher_choice.get() == "Playfair":
            result = self.playfair_encrypt(message, key)
        else:
            result = self.hill_encrypt(message, key)
        self.result_encrypt.delete(1.0, tk.END)
        self.result_encrypt.insert(tk.END, result)

    def decrypt(self):
        key = self.get_key()
        if key is None:
            return
        message = self.get_message()
        if self.cipher_choice.get() == "Vigenere":
            result = self.vigenere_decrypt(message, key)
        elif self.cipher_choice.get() == "Playfair":
            result = self.playfair_decrypt(message, key)
        else:
            result = self.hill_decrypt(message, key)
        self.result_decrypt.delete(1.0, tk.END)
        self.result_decrypt.insert(tk.END, result)

    def vigenere_encrypt(self, plaintext, key):
        ciphertext = ""
        key_length = len(key)
        key_as_int = [ord(i) for i in key]
        plaintext_int = [ord(i) for i in plaintext]
        for i in range(len(plaintext_int)):
            if plaintext[i].isalpha():
                value = (plaintext_int[i] + key_as_int[i % key_length]) % 256
                ciphertext += chr(value)
            else:
                ciphertext += plaintext[i]
        return ciphertext

    def vigenere_decrypt(self, ciphertext, key):
        plaintext = ""
        key_length = len(key)
        key_as_int = [ord(i) for i in key]
        ciphertext_int = [ord(i) for i in ciphertext]
        for i in range(len(ciphertext_int)):
            if ciphertext[i].isalpha():
                value = (ciphertext_int[i] - key_as_int[i % key_length]) % 256
                plaintext += chr(value)
            else:
                plaintext += ciphertext[i]
        return plaintext

    def playfair_encrypt(self, plaintext, key):
        # Menghapus karakter yang tidak valid dan mengganti J dengan I
        plaintext = plaintext.replace('J', 'I').replace(' ', '').upper()
        key = ''.join(sorted(set(key), key=key.index)).replace('J', 'I').upper()

        # Membuat tabel Playfair
        table = self.create_playfair_table(key)
        ciphertext = ""

        # Membentuk pasangan karakter
        pairs = self.form_pairs(plaintext)

        for a, b in pairs:
            row1, col1 = divmod(table.index(a), 5)
            row2, col2 = divmod(table.index(b), 5)

            if row1 == row2:
                ciphertext += table[row1 * 5 + (col1 + 1) % 5]
                ciphertext += table[row2 * 5 + (col2 + 1) % 5]
            elif col1 == col2:
                ciphertext += table[((row1 + 1) % 5) * 5 + col1]
                ciphertext += table[((row2 + 1) % 5) * 5 + col2]
            else:
                ciphertext += table[row1 * 5 + col2]
                ciphertext += table[row2 * 5 + col1]

        return ciphertext
    
    def playfair_decrypt(self, ciphertext, key):
        # Menghapus karakter yang tidak valid dan mengganti J dengan I
        key = ''.join(sorted(set(key), key=key.index)).replace('J', 'I').upper()
        table = self.create_playfair_table(key)
        plaintext = ""

        pairs = self.form_pairs(ciphertext)

        for a, b in pairs:
            row1, col1 = divmod(table.index(a), 5)
            row2, col2 = divmod(table.index(b), 5)

            if row1 == row2:
                plaintext += table[row1 * 5 + (col1 - 1) % 5]
                plaintext += table[row2 * 5 + (col2 - 1) % 5]
            elif col1 == col2:
                plaintext += table[((row1 - 1) % 5) * 5 + col1]
                plaintext += table[((row2 - 1) % 5) * 5 + col2]
            else:
                plaintext += table[row1 * 5 + col2]
                plaintext += table[row2 * 5 + col1]

        return plaintext

    def create_playfair_table(self, key):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # J dihilangkan
        key = ''.join(sorted(set(key), key=key.index))  # Menghilangkan duplikat
        key += ''.join([ch for ch in alphabet if ch not in key])  # Menambahkan sisa huruf
        return key

    def form_pairs(self, plaintext):
        pairs = []
        i = 0
        while i < len(plaintext):
            a = plaintext[i]
            b = 'X' if (i + 1 == len(plaintext)) else plaintext[i + 1]

            if a == b:
                pairs.append((a, 'X'))
                i += 1
            else:
                pairs.append((a, b))
                i += 2

        return pairs

    def hill_encrypt(self, plaintext, key):
        return "Enkripsi Hill Belum Jadi"

    def hill_decrypt(self, ciphertext, key):
        return "Deskripsi Hill Belum Jadi"


if __name__ == "__main__":
    root = tk.Tk()
    app = CipherApp(root)
    root.mainloop()
