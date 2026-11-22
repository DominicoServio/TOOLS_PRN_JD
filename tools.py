import streamlit as st
import pandas as pd
import re

st.title("Job Description Converter")

uploaded_file = st.file_uploader(
    "Upload JD CSV",
    type=["csv"]
)

if uploaded_file:

    jd = pd.read_csv(uploaded_file)

    col_mapping = {
        'TUJUAN JABATAN': 'JD1',
        'TANGGUNG JAWAB UTAMA ': 'JD2',
        'INDIKATOR KERJA': 'JD3',
        'INTERNAL': 'JD4',
        'TUJUAN HUBUNGAN KERJA': 'JD5',
        'EKSTERNAL': 'JD6',
        'TUJUAN HUBUNGAN KERJA2': 'JD7',
        'REKOMENDASI': 'JD8',
        'PENGAMBILAN KEPUTUSAN': 'JD9',
        'TANTANGAN JABATAN': 'JD10',
        'PENDIDIKAN FORMAL (MIN.)': 'JD11',
        'PENGALAMAN KERJA (MIN.)': 'JD12',
        'PELATIHAN WAJIB': 'JD13',
        'KETERAMPILAN TEKNIS (HARD SKILL)': 'JD14',
        'KETERAMPILAN NON TEKNIS (SOFT SKILL)': 'JD15'
    }

    jd = jd[['JABATAN'] + list(col_mapping.keys())]
    jd = jd.rename(columns=col_mapping)

    jd_long = jd.melt(
        id_vars=['JABATAN'],
        var_name='COLUMN',
        value_name='VALUE'
    )

    jd_long = jd_long.fillna('')

    def normalize_text(s):
        s = str(s).lower()
        s = re.sub(r'[^\w\s]', '', s)
        s = re.sub(r'\s+', ' ', s)
        return s.strip()

    def clean_text(t):
        t = re.sub(r'\s+', ' ', str(t))
        return t.strip()

    jd_long['VAL_CLEAN'] = jd_long['VALUE'].apply(normalize_text)

    jd_long = jd_long.drop_duplicates(
        subset=['JABATAN','COLUMN','VAL_CLEAN']
    )

    jd_long['VALUE'] = jd_long['VALUE'].apply(clean_text)

    jd_long = jd_long[jd_long['VALUE'] != '']

    jd_long['NUMBER'] = (
        jd_long.groupby(['JABATAN','COLUMN'])
        .cumcount() + 1
    )

    jd_long['COL_NUM'] = (
        jd_long['COLUMN']
        .str.extract(r'(\d+)')
        .astype(int)
    )

    jd_long = (
        jd_long
        .sort_values(['JABATAN','COL_NUM','NUMBER'])
    )

    final_jd = jd_long[
        ['JABATAN','COLUMN','NUMBER','VALUE']
    ]

    output = final_jd.to_csv(
        sep="\t",
        index=False,
        header=False
    )

    st.download_button(
        "Download TXT",
        output,
        file_name="uplmstrjobdesc.txt"
    )
