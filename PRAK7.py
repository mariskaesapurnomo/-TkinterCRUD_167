import sqlite3    # Import modul sqlite3 untuk mengelola database SQLite.
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk    # Import modul tkinter untuk membuat antarmuka pengguna grafis (GUI).

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')    # Membuka koneksi ke database bernama 'nilai_siswa.db'
    cursor = conn.cursor()  # Membuat objek cursor untuk mengeksekusi perintah SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')        # Perintah SQL untuk membuat tabel 'nilai_siswa' jika belum ada
    conn.commit()    # Menyimpan perubahan ke database.
    conn.close()    # Menutup koneksi ke database.

# Fungsi untuk Mengambil semua data dari tabel nilai_siswa
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')    # Membuka koneksi ke database
    cursor = conn.cursor()                      # Membuat objek cursor untuk mengeksekusi perintah SQL
    cursor.execute("SELECT * FROM nilai_siswa") # Menjalankan perintah SQL untuk memilih semua data dari tabel.
    rows = cursor.fetchall()                    # Mengambil semua data hasil query dalam bentuk list.
    conn.close()                                # Menutup koneksi ke database.
    return rows                                 # Mengembalikan data dalam bentuk list.# Mengembalikan data dalam bentuk list.

# Fungsi untuk Menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')    # Membuka koneksi ke database.
    cursor = conn.cursor()                      # Membuat objek cursor untuk mengeksekusi perintah SQL.
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))    # Menjalankan perintah SQL untuk memasukkan data baru ke tabel.
    conn.commit()        # Menyimpan perubahan ke database.
    conn.close()         # Menutup koneksi ke database.

#Fungsi untuk Memperbarui data yang sudah ada di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')      # Membuka koneksi ke database.
    cursor = conn.cursor()                        # Membuat objek cursor untuk mengeksekusi perintah SQL.
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id)) # Menjalankan perintah SQL untuk memperbarui data berdasarkan ID.
    conn.commit()   # Menyimpan perubahan ke database.
    conn.close()    # Menutup koneksi ke database.

# Fungsi untuk Menghapus record dari database berdasarkan ID
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')        # Membuka koneksi ke database.
    cursor = conn.cursor()                          # Membuat objek cursor untuk mengeksekusi perintah SQL.
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))    # Menjalankan perintah SQL untuk menghapus data berdasarkan ID.
    conn.commit()   # Menyimpan perubahan ke database
    conn.close()    # Menutup koneksi ke database.

# Fungsi untuk Menghitung prediksi fakultas berdasarkan nilai tertinggi
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran" # Prediksi Kedokteran jika nilai biologi tertinggi.
    elif fisika > biologi and fisika > inggris:
        return "Teknik"     # Prediksi Teknik jika nilai fisika tertinggi.
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"     # Prediksi Bahasa jika nilai Inggris tertinggi.
    else:
        return "Tidak Diketahui"    # Prediksi tidak dapat ditentukan.
    
# Fungsi untuk menangani event saat tombol "Add" diklik.
def submit():
    try:
        # Mengambil data dari input pengguna.
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        # Validasi input nama.
        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)   # Menghitung prediksi fakultas berdasarkan nilai.
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Menyimpan data ke database.

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")    # Menampilkan pesan sukses.
        clear_inputs()       # Membersihkan input.
        populate_table()     # Memperbarui tabel tampilan.
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")    # Menampilkan pesan error jika input tidak valid.

# Fungsi untuk memperbarui data yang dipilih di database
def update():
    try:
        # Memastikan ada data yang dipilih untuk di-update.    
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())   # Mengambil ID record yang dipilih dari variabel `selected_record_id`.
        nama = nama_var.get()                        # Mengambil input dari field input nama siswa.
        biologi = int(biologi_var.get())     # Mengambil input nilai biologi serta mengonversinya ke integer.
        fisika = int(fisika_var.get())       # Mengambil input nilai fisika serta mengonversinya ke integer. 
        inggris = int(inggris_var.get())     # Mengambil input nilai inggris serta mengonversinya ke integer.

        # Validasi bahwa nama siswa tidak boleh kosong.
        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)              # Menghitung prediksi fakultas berdasarkan nilai yang diinput.
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)   # Memperbarui data ke database dengan memanggil fungsi `update_database`.

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")      # Menampilkan pesan sukses bahwa data telah diperbarui.
        clear_inputs()           # Membersihkan input field setelah update.
        populate_table()         # Memperbarui tampilan tabel dengan data terbaru.
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")  # Menangkap error jika terjadi kesalahan pada input data, seperti format nilai yang salah.

# Fungsi untuk menghapus record dari database berdasarkan ID yang dipilih.
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")     # Memastikan ada data yang dipilih untuk dihapus.

        record_id = int(selected_record_id.get())       # Mengambil ID record yang dipilih dari variabel `selected_record_id`
        delete_database(record_id)                      # Memanggil fungsi `delete_database` untuk menghapus data dari database.
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")     # Menampilkan pesan sukses bahwa data telah dihapus.
        clear_inputs()       # Membersihkan input field setelah data dihapus.
        populate_table()     # Memperbarui tampilan tabel dengan data terbaru.
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")         # Menangkap error jika terjadi kesalahan dalam proses penghapusan.

# Fungsi untuk Membersihkan semua input field
def clear_inputs():
    nama_var.set("")        # Mengatur input nama menjadi string kosong.
    biologi_var.set("")     # Mengatur input nilai biologi menjadi string kosong.
    fisika_var.set("")      # Mengatur input nilai fisika menjadi string kosong.
    inggris_var.set("")     # Mengatur input nilai Inggris menjadi string kosong.
    selected_record_id.set("")  # Menghapus ID record yang dipilih.

#Fungsi untuk Memperbarui tampilan tabel dengan data terbaru dari database
def populate_table():
    for row in tree.get_children():
        tree.delete(row)    # Menghapus semua data yang ada di tabel GUI.
    for row in fetch_data():    # Mengambil data terbaru dari database.
        tree.insert('', 'end', values=row)  # Menambahkan setiap baris data ke dalam tabel GUI.

#Fungsi untuk Mengisi form input dengan data yang dipilih dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]      # Mendapatkan item yang dipilih dari tabel GUI.
        selected_row = tree.item(selected_item)['values']       # Mengambil nilai dari baris yang dipilih.

         # Mengisi input field dengan data dari baris yang dipilih.
        selected_record_id.set(selected_row[0]) # ID record.
        nama_var.set(selected_row[1])       # Nama siswa.
        biologi_var.set(selected_row[2])    # Nilai biologi.
        fisika_var.set(selected_row[3])     # Nilai fisika.
        inggris_var.set(selected_row[4])    # Nilai inggris.
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")    # Menampilkan pesan error jika tidak ada data yang valid dipilih.

# Inisialisasi database dengan memanggil fungsi `create_database`
create_database()

# Membuat GUI dengan tkinter
root = Tk()     # Inisialisasi jendela utama aplikasi.
root.title("Prediksi Fakultas Siswa")      # Menentukan judul jendela.

# Variabel tkinter untuk mengelola input pengguna.
nama_var = StringVar()      # Variabel untuk input nama siswa.
biologi_var = StringVar()   # Variabel untuk input nilai biologi.
fisika_var = StringVar()    # Variabel untuk input nilai fisika.
inggris_var = StringVar()   # Variabel untuk input nilai Inggris.
selected_record_id = StringVar()  # Variabel Untuk menyimpan ID record yang dipilih

# Menambahkan label dan input field ke jendela utama.
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

#  Tombol-tombol aksi  untuk Add, Update, dan Delete.
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')      # Membuat tabel dengan kolom tertentu.

# Menentukan nama kolom dan posisi isi tabel.
for col in columns:
    tree.heading(col, text=col.capitalize())     # Menambahkan judul kolom.
    tree.column(col, anchor='center')   # Mengatur posisi isi tabel di tengah

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)   # Menampilkan tabel pada GUI.

# Menambahkan event handler untuk klik pada tabel
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Memuat data awal ke tabel
populate_table()

# Memulai aplikasi
root.mainloop()
