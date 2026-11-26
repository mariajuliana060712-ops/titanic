# Praktik Streamlit Bab 1–2 — Dataset Titanic

Project ini menggunakan **dataset Titanic yang kamu upload**, bukan data dummy.

## Isi folder

- `hello_world.py` — praktik aplikasi Streamlit pertama (Bab 1).
- `main.py` — praktik materi Streamlit Bab 2 dalam satu aplikasi.
- `data/titanic.csv` — dataset asli yang kamu berikan.
- `requirements.txt` — daftar library.

## 1. Buka project di VS Code

1. Extract ZIP ini.
2. Buka VS Code.
3. Pilih **File → Open Folder**.
4. Pilih folder `Praktik_Streamlit_Titanic_Bab1-2`.

## 2. Buat virtual environment (disarankan)

Buka Terminal di VS Code, lalu jalankan:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Jika PowerShell menolak aktivasi, jalankan terminal CMD atau gunakan:

```powershell
.venv\\Scripts\\python.exe -m pip install -r requirements.txt
```

## 3. Install library

```powershell
python -m pip install -r requirements.txt
```

## 4. Jalankan Bab 1

```powershell
python -m streamlit run hello_world.py
```

## 5. Jalankan seluruh praktik Bab 2

Hentikan aplikasi sebelumnya dengan `Ctrl + C`, lalu:

```powershell
python -m streamlit run main.py
```

Streamlit akan menampilkan alamat lokal, biasanya `http://localhost:8501`.

## Catatan dataset

Hasil pemeriksaan dataset:
- 891 baris dan 12 kolom.
- Kolom: `PassengerId`, `Survived`, `Pclass`, `Name`, `Sex`, `Age`, `SibSp`, `Parch`, `Ticket`, `Fare`, `Cabin`, `Embarked`.
- Nilai kosong: `Age` 177, `Cabin` 687, `Embarked` 2.
- Kolom `Survived`: 0 = tidak selamat, 1 = selamat.

Aplikasi mempertahankan data asli. Untuk filter umur, nilai umur kosong tidak dimasukkan ke hasil filter. Statistik dan visualisasi yang membutuhkan umur hanya menggunakan nilai umur yang tersedia.

## Penyesuaian API Streamlit

Modul yang lebih lama mungkin memakai:
- `st.experimental_data_editor()` → sekarang gunakan `st.data_editor()`.
- `st.experimental_rerun()` → sekarang gunakan `st.rerun()`.

## Batasan yang perlu diketahui

- Dataset Titanic tidak memiliki koordinat latitude/longitude, jadi `st.map()` tidak bisa menampilkan lokasi penumpang secara akurat. Aplikasi menjelaskan alasan bagian peta dilewati.
- Dataset tidak berisi file gambar, audio, atau video. Widget media disediakan agar kamu bisa mengunggah file sendiri untuk mempraktikkan `st.image`, `st.audio`, dan `st.video`.
- `st.camera_input()` membutuhkan izin kamera dari browser.
- `st.data_editor()` tidak menimpa file CSV asli.
