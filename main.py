
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

from pathlib import Path
from datetime import date, time


# =====================================================
# 1. KONFIGURASI APLIKASI
# =====================================================

st.set_page_config(
    page_title="Analisis Dataset Titanic",
    page_icon="🚢",
    layout="wide"
)


# =====================================================
# 2. MEMBACA DATASET
# =====================================================

BASE_DIR = Path(__file__).parent

# Mencari file CSV di beberapa kemungkinan lokasi
possible_paths = [
    BASE_DIR / "data" / "titanic.csv",
    BASE_DIR / "data" / "titanic(1).csv",
    BASE_DIR / "titanic.csv",
    BASE_DIR / "titanic(1).csv"
]

DATA_PATH = next(
    (path for path in possible_paths if path.exists()),
    None
)


@st.cache_data
def load_data(path):
    return pd.read_csv(path)


st.title("🚢 Analisis Data Penumpang Titanic")
st.write(
    "Aplikasi praktik Streamlit Bab 1–2 menggunakan "
    "dataset Titanic."
)

st.divider()

if DATA_PATH is None:
    st.error(
        "File Titanic tidak ditemukan. "
        "Simpan file CSV di folder data dengan nama titanic.csv."
    )
    st.stop()

df = load_data(str(DATA_PATH))


# =====================================================
# 3. ELEMEN TEKS STREAMLIT
# =====================================================

st.header("1. Praktik Elemen Teks")

with st.expander("Klik untuk melihat contoh elemen teks"):
    st.title("Contoh st.title()")
    st.header("Contoh st.header()")
    st.subheader("Contoh st.subheader()")

    st.markdown("**Contoh teks tebal menggunakan Markdown**")
    st.caption("Contoh caption atau keterangan kecil.")
    st.text("Contoh teks biasa.")
    st.code("print('Hello Streamlit!')", language="python")
    st.latex(r"P(Survived=1) = \frac{\text{Jumlah selamat}}{\text{Jumlah penumpang}}")

    st.write("Contoh penggunaan st.write().")


# =====================================================
# 4. INFORMASI DAN TAMPILAN DATA
# =====================================================

st.header("2. Informasi Dataset")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Jumlah Penumpang", len(df))
col2.metric("Jumlah Kolom", len(df.columns))

if "Survived" in df.columns:
    col3.metric(
        "Selamat",
        int((df["Survived"] == 1).sum())
    )
    col4.metric(
        "Tidak Selamat",
        int((df["Survived"] == 0).sum())
    )

tab1, tab2, tab3 = st.tabs(
    ["DataFrame", "Table", "JSON"]
)

with tab1:
    st.subheader("Tampilan DataFrame")
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Tampilan Tabel")
    st.table(df.head(20))

with tab3:
    st.subheader("Tampilan JSON")
    st.json(df.head(3).to_dict(orient="records"))

st.subheader("Statistik Dataset")
st.write(df.describe(include="all"))


# =====================================================
# 5. VISUALISASI DATA
# =====================================================

st.header("3. Praktik Visualisasi Data")

if "Survived" in df.columns:

    survival_count = (
        df["Survived"]
        .map({0: "Tidak Selamat", 1: "Selamat"})
        .value_counts()
        .rename_axis("Status")
        .reset_index(name="Jumlah")
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Bar Chart")
        st.bar_chart(
            survival_count.set_index("Status")
        )

    with col2:
        st.subheader("Pie Chart")
        pie_data = survival_count
        fig_pie = px.pie(
            pie_data,
            names="Status",
            values="Jumlah",
            title="Persentase Keselamatan"
        )
        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

if "Pclass" in df.columns:
    st.subheader("Line Chart")

    class_count = (
        df["Pclass"]
        .value_counts()
        .sort_index()
    )

    st.line_chart(class_count)

if "Age" in df.columns:
    st.subheader("Area Chart")

    age_data = df["Age"].dropna()

    age_hist = (
        pd.cut(age_data, bins=10)
        .value_counts()
        .sort_index()
    )

    age_chart = pd.DataFrame({
        "Rentang Umur": age_hist.index.astype(str),
        "Jumlah": age_hist.values
    })

    st.area_chart(
        age_chart.set_index("Rentang Umur")
    )

if all(col in df.columns for col in ["Sex", "Survived"]):

    st.subheader("Altair Chart")

    gender_data = (
        df.groupby(["Sex", "Survived"])
        .size()
        .reset_index(name="Jumlah")
    )

    alt_chart = (
        alt.Chart(gender_data)
        .mark_bar()
        .encode(
            x=alt.X("Sex:N", title="Gender"),
            y=alt.Y("Jumlah:Q"),
            color=alt.Color("Survived:N"),
            tooltip=["Sex", "Survived", "Jumlah"]
        )
    )

    st.altair_chart(
        alt_chart,
        use_container_width=True
    )

    st.subheader("Plotly Chart")

    plot_data = gender_data.copy()
    plot_data["Status"] = plot_data["Survived"].map({
        0: "Tidak Selamat",
        1: "Selamat"
    })

    fig = px.bar(
        plot_data,
        x="Sex",
        y="Jumlah",
        color="Status",
        barmode="group",
        title="Keselamatan Berdasarkan Gender"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.subheader("Peta")
st.info(
    "Dataset Titanic tidak memiliki koordinat latitude "
    "dan longitude, sehingga data tidak dapat ditampilkan "
    "pada peta secara akurat."
)


# =====================================================
# 6. INPUT DAN FILTER
# =====================================================

st.header("4. Praktik Input dan Filter")

with st.sidebar:
    st.title("⚙️ Filter Dataset")

    if "Sex" in df.columns:
        selected_sex = st.multiselect(
            "Pilih Gender",
            options=sorted(df["Sex"].dropna().unique()),
            default=sorted(df["Sex"].dropna().unique())
        )
    else:
        selected_sex = None

    if "Pclass" in df.columns:
        selected_class = st.multiselect(
            "Pilih Kelas",
            options=sorted(df["Pclass"].dropna().unique()),
            default=sorted(df["Pclass"].dropna().unique())
        )
    else:
        selected_class = None

    survival_option = st.selectbox(
        "Status Keselamatan",
        ["Semua", "Selamat", "Tidak Selamat"]
    )

    if "Age" in df.columns:
        max_age = int(df["Age"].max())
        age_range = st.slider(
            "Rentang Umur",
            min_value=0,
            max_value=max_age,
            value=(0, max_age)
        )

filtered = df.copy()

if selected_sex is not None:
    filtered = filtered[
        filtered["Sex"].isin(selected_sex)
    ]

if selected_class is not None:
    filtered = filtered[
        filtered["Pclass"].isin(selected_class)
    ]

if "Age" in df.columns:
    filtered = filtered[
        filtered["Age"].fillna(-1).between(
            age_range[0],
            age_range[1]
        )
    ]

if "Survived" in df.columns:
    if survival_option == "Selamat":
        filtered = filtered[filtered["Survived"] == 1]
    elif survival_option == "Tidak Selamat":
        filtered = filtered[filtered["Survived"] == 0]

st.write(f"Jumlah data setelah filter: **{len(filtered)}**")
st.dataframe(filtered, use_container_width=True)


# Contoh widget lainnya
with st.expander("Contoh Widget Input Lainnya"):

    st.subheader("Checkbox")

    show_preview = st.checkbox(
        "Tampilkan 5 data pertama",
        value=True
    )

    if show_preview:
        st.dataframe(df.head())

    st.subheader("Radio Button")

    radio_choice = st.radio(
        "Pilih kolom",
        df.columns.tolist(),
        horizontal=True
    )

    st.write("Kolom dipilih:", radio_choice)

    st.subheader("Selectbox")

    selected_column = st.selectbox(
        "Pilih kolom dataset",
        df.columns.tolist()
    )

    st.write(df[selected_column].head())

    st.subheader("Text Input")

    search_name = st.text_input(
        "Cari nama penumpang"
    )

    if search_name and "Name" in df.columns:
        search_result = df[
            df["Name"].str.contains(
                search_name,
                case=False,
                na=False
            )
        ]
        st.dataframe(search_result)

    st.subheader("Number Input")

    passenger_id = st.number_input(
        "Masukkan Passenger ID",
        min_value=1,
        value=1
    )

    st.write("Passenger ID:", passenger_id)

    st.subheader("Text Area")

    notes = st.text_area(
        "Tulis catatan praktik"
    )

    st.write("Jumlah karakter:", len(notes))

    st.subheader("Date Input dan Time Input")

    selected_date = st.date_input(
        "Pilih tanggal",
        value=date.today()
    )

    selected_time = st.time_input(
        "Pilih waktu",
        value=time(9, 0)
    )

    st.write(selected_date, selected_time)

    st.subheader("Color Picker")

    picked_color = st.color_picker(
        "Pilih warna",
        "#1f77b4"
    )

    st.write("Warna yang dipilih:", picked_color)


# =====================================================
# 7. DATA EDITOR DAN DOWNLOAD
# =====================================================

st.header("5. Edit dan Download Data")

st.subheader("Data Editor")

st.caption(
    "Perubahan di sini hanya berlaku pada tampilan aplikasi "
    "dan tidak mengubah file CSV asli."
)

edited_df = st.data_editor(
    df.head(20),
    use_container_width=True,
    num_rows="dynamic"
)

st.subheader("Download CSV")

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Hasil Filter",
    data=csv_data,
    file_name="titanic_hasil_filter.csv",
    mime="text/csv"
)


# =====================================================
# 8. FILE UPLOADER DAN CAMERA INPUT
# =====================================================

st.header("6. File Uploader dan Camera Input")

uploaded_csv = st.file_uploader(
    "Upload file CSV",
    type=["csv"]
)

if uploaded_csv is not None:
    uploaded_df = pd.read_csv(uploaded_csv)

    st.success("File berhasil dibaca!")
    st.dataframe(
        uploaded_df.head(),
        use_container_width=True
    )

st.subheader("Camera Input")

camera_photo = st.camera_input(
    "Ambil foto menggunakan kamera"
)

if camera_photo is not None:
    st.image(
        camera_photo,
        caption="Foto dari kamera",
        use_container_width=True
    )


# =====================================================
# 9. MENAMPILKAN MEDIA
# =====================================================

st.header("7. Praktik Menampilkan Media")

st.write(
    "Bagian ini digunakan untuk mencoba menampilkan "
    "gambar, audio, dan video."
)

st.subheader("Menampilkan Gambar")

image_file = st.file_uploader(
    "Upload gambar",
    type=["png", "jpg", "jpeg"],
    key="media_image"
)

if image_file:
    st.image(
        image_file,
        caption="Contoh st.image()",
        use_container_width=True
    )

st.subheader("Menampilkan Audio")

audio_file = st.file_uploader(
    "Upload audio",
    type=["mp3", "wav", "ogg"],
    key="media_audio"
)

if audio_file:
    st.audio(audio_file)

st.subheader("Menampilkan Video")

video_file = st.file_uploader(
    "Upload video",
    type=["mp4", "mov", "webm"],
    key="media_video"
)

if video_file:
    st.video(video_file)


# =====================================================
# 10. PRAKTIK LAYOUT
# =====================================================

st.header("8. Praktik Layout Streamlit")

st.write(
    "Layout digunakan untuk mengatur posisi dan susunan "
    "komponen agar aplikasi lebih rapi."
)

layout_tab1, layout_tab2, layout_tab3 = st.tabs([
    "Columns",
    "Container",
    "Expander"
])

# COLUMNS
with layout_tab1:
    st.subheader("Contoh st.columns()")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("Kolom Pertama")
        st.write("Ini adalah bagian kiri.")

    with col2:
        st.success("Kolom Kedua")
        st.write("Ini adalah bagian tengah.")

    with col3:
        st.warning("Kolom Ketiga")
        st.write("Ini adalah bagian kanan.")

# CONTAINER
with layout_tab2:
    st.subheader("Contoh st.container()")

    with st.container(border=True):
        st.write("Ini adalah container.")
        st.write("Komponen dikelompokkan dalam satu area.")

        container_col1, container_col2 = st.columns(2)

        container_col1.metric(
            "Jumlah Data",
            len(df)
        )

        container_col2.metric(
            "Jumlah Kolom",
            len(df.columns)
        )

# EXPANDER
with layout_tab3:
    st.subheader("Contoh st.expander()")

    with st.expander("Klik untuk membuka informasi"):
        st.write("Ini adalah isi dari expander.")
        st.write(
            "Expander digunakan untuk menyembunyikan "
            "atau menampilkan konten."
        )


st.subheader("Contoh st.empty()")

placeholder = st.empty()
placeholder.info(
    "Ini adalah placeholder menggunakan st.empty()."
)

if st.button("Ubah Isi Placeholder"):
    placeholder.success(
        "Isi placeholder berhasil diubah!"
    )


# =====================================================
# 11. FORM DAN CONTROL FLOW
# =====================================================

st.header("9. Form dan Control Flow")

with st.form("contoh_form"):

    st.subheader("Form Praktikan")

    form_name = st.text_input(
        "Masukkan nama"
    )

    form_topic = st.selectbox(
        "Materi yang paling dipahami",
        [
            "Elemen Teks",
            "DataFrame",
            "Visualisasi",
            "Input Widget",
            "Layout"
        ]
    )

    submitted = st.form_submit_button(
        "Kirim"
    )

if submitted:
    st.success(
        f"Terima kasih {form_name or 'praktikan'}! "
        f"Materi pilihan: {form_topic}."
    )

st.subheader("Contoh st.rerun()")

if st.button("Jalankan Rerun"):
    st.rerun()

st.subheader("Contoh st.stop()")

if st.button("Hentikan Aplikasi"):
    st.warning(
        "Aplikasi dihentikan menggunakan st.stop()."
    )
    st.stop()


# =====================================================
# 12. FOOTER
# =====================================================

st.divider()

st.caption(
    "Praktik Streamlit Bab 1–2 | Dataset Titanic"
)
