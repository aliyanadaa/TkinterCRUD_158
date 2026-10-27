import tkinter as tk
from tkinter import messagebox
import sqlite3

# Membuat database dan tabel
def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_db()


# Fungsi untuk menghitung prediksi dan menyimpan data
def prediksi_fakultas(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Dapat Ditentukan"

# Fungsi untuk menghitung prediksi dan menyimpan data
def submit_nilai():
    nama = entry_nama.get().strip()
    try:
        biologi = int(entry_biologi.get())
        fisika = int(entry_fisika.get())
        inggris = int(entry_inggris.get())
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")
        return

    if not nama:
        messagebox.showerror("Error", "Nama siswa harus diisi!")
        return

    if not all(0 <= nilai <= 100 for nilai in
               [biologi, fisika, inggris]):
        messagebox.showerror("Error", "Nilai harus 0-100!")
        return

    hasil_prediksi = prediksi_fakultas(biologi, fisika, inggris)

    # Menyimpan data ke SQLite
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, hasil_prediksi))
    conn.commit()
    conn.close()

    messagebox.showinfo("Hasil Prediksi", f"Prediksi Fakultas untuk {nama}: {hasil_prediksi} ")

# Membuat tampilan Tkinter
root = tk.Tk()
root.title("Aplikasi Prediksi Prodi Pilihan")
root.geometry("350x300")

tk.Label(root, text="Aplikasi Prediksi Prodi Pilihan").grid(
    row=0, column=0, columnspan=2, pady=10
)

tk.Label(root, text="Nama Siswa").grid(row=1, column=0, padx=10, pady=5)
entry_nama = tk.Entry(root)
entry_nama.grid(row=1, column=1, pady=5)

tk.Label(root, text="Biologi").grid(row=2, column=0, padx=10, pady=5)
entry_biologi = tk.Entry(root)
entry_biologi.grid(row=2, column=1, pady=5)

tk.Label(root, text="Fisika").grid(row=3, column=0, padx=10, pady=5)
entry_fisika = tk.Entry(root)
entry_fisika.grid(row=3, column=1, pady=5)

tk.Label(root, text="Inggris").grid(row=4, column=0, padx=10, pady=5)
entry_inggris = tk.Entry(root)
entry_inggris.grid(row=4, column=1, pady=5)

tk.Button(root, text="Hasil Prediksi",
          command=submit_nilai).grid(
    row=5, column=0, columnspan=2, pady=10
)

label_hasil = tk.Label(root, text="Prediksi Fakultas: ")
label_hasil.grid(row=6, column=0, columnspan=2, pady=5)

root.mainloop()
