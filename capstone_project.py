import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from scipy.stats import pearsonr

st.set_page_config(
    page_title="Analisa IPM & Stunting",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")

st.markdown("""<style>.title {text-align: center;}</style>""", unsafe_allow_html=True)
st.markdown("<h1 class='title'>Analisa Indeks Pembangunan Manusia (IPM) dengan Prevalensi Kejadian Stunting</h1>", unsafe_allow_html=True)

# Import Data CSV "ipm.csv"
ipm = pd.read_csv('https://drive.google.com/uc?export=download&id=176hTNv-gzyrjAyVnZ-IS-nWtTcdhhLv7')

# Tabbing
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Angka IPM & Prevalensi Stunting','Tren IPM & Prevalensi Stunting', 'Korelasi IPM & Prevalensi Stunting','Dataset','Referensi'])

with tab1:
    with st.sidebar:
        st.title('Pilih Filter')
    
        # Default Filtering
        default_provinsi = 'INDONESIA'
        default_kab_kota = 'INDONESIA'
        default_tahun = 2022
        default_filter_tahun = ipm[ipm['tahun'] == default_tahun]

        # Filter Tahun
        pilih_tahun = st.selectbox("Pilih Tahun", ipm["tahun"].unique(), index=ipm['tahun'].unique().tolist().index(default_tahun))
        filter_tahun = ipm[ipm['tahun'] == pilih_tahun]
        filter_tahun_sebelum = ipm[ipm['tahun'] == pilih_tahun-1]
        default_filter_area = filter_tahun[(filter_tahun['provinsi'] == default_provinsi) & (filter_tahun['kab_kota'] == default_kab_kota)]

        # Filter Provinsi
        pilih_provinsi = st.selectbox("Pilih Provinsi", filter_tahun[filter_tahun['tahun'] == pilih_tahun]['provinsi'].unique(), index=filter_tahun['provinsi'].unique().tolist().index(default_provinsi))

        # Filter Kabupaten_Kota
        pilih_kab_kota = st.selectbox("Pilih Kabupaten/Kota", filter_tahun[filter_tahun['provinsi'] == pilih_provinsi]['kab_kota'].unique())

    # Judul Contener
    custom_container = st.container(border=True)
    with custom_container:
        st.markdown("""<div style="font-size: 19px; font-weight: bold;">Angka Indeks Pembangunan Manusia (IPM) dan Prevalensi Kejadian 
                    Stunting di <span style="color: green;">{}</span> Tahun <span style="color: green;">{}</span>
        """.format(pilih_kab_kota, pilih_tahun), unsafe_allow_html=True)

    # Kolom Data
    jml_balita, pendek, sangat_pendek, prevalensi, ipm = st.columns(5)

    with jml_balita:
        balita_sekarang = filter_tahun.loc[filter_tahun['kab_kota']==pilih_kab_kota, 'jml_balita'].values[0]
        balita_sebelum = filter_tahun_sebelum.loc[filter_tahun_sebelum['kab_kota']==pilih_kab_kota, 'jml_balita'].values[0]
        selisih_balita = balita_sekarang - balita_sebelum
        st.metric("Jumlah Balita (Anak)", value="{:,.0f}".format(balita_sekarang), delta=f'{"{:,.0f}".format(selisih_balita)}')

    with ipm:
        ipm_sekarang = filter_tahun.loc[filter_tahun['kab_kota']==pilih_kab_kota, 'ipm'].values[0]
        ipm_sebelum = filter_tahun_sebelum.loc[filter_tahun_sebelum['kab_kota']==pilih_kab_kota, 'ipm'].values[0]
        selisih_ipm = ipm_sekarang - ipm_sebelum
        st.metric("IPM", value=f'{ipm_sekarang:.2f}', delta=f'{selisih_ipm:.2f}')

    with prevalensi:
        prevalensi_sekarang = filter_tahun.loc[filter_tahun['kab_kota']==pilih_kab_kota, 'prev_stunting'].values[0]
        prevalensi_sebelum = filter_tahun_sebelum.loc[filter_tahun_sebelum['kab_kota']==pilih_kab_kota, 'prev_stunting'].values[0]
        selisih_prevalensi = prevalensi_sekarang - prevalensi_sebelum
        st.metric("Prevalensi Stunting", value=f'{prevalensi_sekarang:.2f}%', delta=f'{selisih_prevalensi:.2f}%')

    with pendek:
        pendek_sekarang = filter_tahun.loc[filter_tahun['kab_kota']==pilih_kab_kota, 'balita_pendek'].values[0]
        pendek_sebelum = filter_tahun_sebelum.loc[filter_tahun_sebelum['kab_kota']==pilih_kab_kota, 'balita_pendek'].values[0]
        selisih_pendek = pendek_sekarang - pendek_sebelum
        st.metric("Balita Pendek", value="{:,.0f}".format(pendek_sekarang), delta=f'{"{:,.0f}".format(selisih_pendek)}')

    with sangat_pendek:
        sangat_pendek_sekarang = filter_tahun.loc[filter_tahun['kab_kota']==pilih_kab_kota, 'balita_sangat_pendek'].values[0]
        sangat_pendek_sebelum = filter_tahun_sebelum.loc[filter_tahun_sebelum['kab_kota']==pilih_kab_kota, 'balita_sangat_pendek'].values[0]
        selisih_sangat_pendek = sangat_pendek_sekarang - sangat_pendek_sebelum
        st.metric("Balita Pendek", value="{:,.0f}".format(sangat_pendek_sekarang), delta=f'{"{:,.0f}".format(selisih_sangat_pendek)}')

    # Teks Tab1
    col1 = st.container(border=True)
    with col1:     
        st.markdown("""
                    <p style="text-align: justify;">
                    <strong><span style="color: green;">Indeks Pembangunan Manusia (IPM)</span></strong>
                    mengukur capaian pembangunan manusia berbasis sejumlah komponen dasar kualitas
                    hidup. Sebagai ukuran kualitas hidup, IPM dibangun melalui pendekatan tiga dimensi dasar. Dimensi tersebut mencakup umur 
                    panjang dan sehat; pengetahuan, dan kehidupan yang layak.
                    <strong><span style="color: green;">Stunting</span></strong> terjadi karena adanya hambatan pertumbuhan pada anak usia di bawah 24 bulan, yang 
                    ditandai dengan pendeknya panjang badan bila dibandingkan perkembangan usia. Salah satu penyebabnya adalah rendahnya asupan gizi, sejak di dalam kandungan
                    ibunya, sampai pada 24 bulan setelah kelahiran.
                    </div>""", unsafe_allow_html=True)
with tab2:
    st.markdown("""<style>.subheader {text-align: center;font-size: 1.4em;}</style>""", unsafe_allow_html=True)
    st.markdown("<h2 class='subheader'>Tren Indeks Pembangunan Manusia (IPM) dan Prevalensi Kejadian Stunting Tahun 2018-2022</h2>", unsafe_allow_html=True)

    col2 = st.container(border=True)
    with col2:
    #     st.markdown(""" Kemiskinan dan termasuk kekurangan gizi menjadi prioritas pertama dalam program 
    #                 _Sustainable Development Goals (SDGs)_ Perserikatan BangsaBangsa. Karena akan mempengaruhi 
    #                 tingkat kualitas manusia, yang akhirnya akan mempengaruhi produktivitas ekonomi. __<span style="color:green;">Indeks Pembangunan Manusia (IPM)</span>__
    #                 </div>""", unsafe_allow_html=True)
        
        st.markdown("""
                    <p style="text-align: justify;">
                    Stunting adalah gangguan pertumbuhan pada anak akibat dari kurangnya asupan gizi dalam waktu yang cukup lama 
                    menyebabkan tinggi badan anak lebih pendek dari standar tinggi badan anak seusianya (Kemenkes, 2018). Anak-anak 
                    merupakan aset paling penting dalam pembangunan suatu negara yang perlu dijaga. Namun, berdasarkan hasil Riset 
                    Kesehatan Dasar (RISKESDA) tahun 2018 prevalensi kejadian stunting di Indonesia mencapai 30,8 persen dimana 
                    sekitar <strong><span style="color: green;">30 dari setiap 100 anak balita di Indonesia mengalami stunting</span></strong>. Berdasarkan data E-Monev Terintegrasi 
                    Kementerian Dalam Negeri pada tahun 2019 prevalensi kejadian stunting mengalami penurunan. Prevalensi stunting 
                    turun sebesar 18,7 persen pada tahun 2019, 1,2 persen pada tahun 2020, 1,4 persen pada tahun 2021 dan 1,1 persen 
                    pada tahun 2022. Sehingga akan prevalensi kejadian stunting Indonesia pada tahun 2022 sebesar 8,4 persen.
                    </p>""", unsafe_allow_html=True)

    # Chart Scatter 1 = IPM VS PREVALENSI STUNTING
    chart = pd.read_csv('https://drive.google.com/uc?export=download&id=176hTNv-gzyrjAyVnZ-IS-nWtTcdhhLv7')
    tren_ipm, tren_stunting = st.columns(2)

    with tren_ipm:    
        chart['tahun'] = pd.to_datetime(chart['tahun'], format='%Y')
        ipm_line = alt.Chart(chart[chart['provinsi']=='INDONESIA']).mark_line(color='green').encode(
        x=alt.X('tahun:T', title=None,axis=alt.Axis(format='%Y', tickCount=5)),
        y=alt.Y('ipm:Q', scale=alt.Scale(domain=[70, 74]), title='Indeks Pembangunan Manusia')
        ).properties(title='Tren Indeks Pembangunan Manusia INDONESIA Tahun 2018-2022',
        width=600,
        height=350
        )
        ipm_point = alt.Chart(chart[chart['provinsi']=='INDONESIA']).mark_point(size=30).encode(
        x=alt.X('tahun:T',axis=alt.Axis(format='%Y')),
        y='ipm:Q'
        )
        combined_chart = ipm_line + ipm_point
        st.altair_chart(combined_chart,use_container_width=True)

    with tren_stunting:
        stunting_line = alt.Chart(chart[chart['provinsi']=='INDONESIA']).mark_line(color='green').encode(
        x=alt.X('tahun:T', title=None,axis=alt.Axis(format='%Y', tickCount=5)),
        y=alt.Y('prev_stunting:Q',scale=alt.Scale(domain=[5, 35]), title='Prevalensi Stunting')
        ).properties(title='Tren Prevalensi Stunting INDONESIA Tahun 2018-2022',
        width=600,
        height=350
        )
        stunting_point = alt.Chart(chart[chart['provinsi']=='INDONESIA']).mark_point(size=30).encode(
        x=alt.X('tahun:T',axis=alt.Axis(format='%Y')),
        y='prev_stunting:Q'
        )
        combined_chart2 = stunting_line + stunting_point
        st.altair_chart(combined_chart2,use_container_width=True)

    col3 = st.container(border=True)
    with col3:
        st.markdown("""
                    <p style="text-align: justify;">
                    Indeks Pembangunan Manusia (IPM) merupakan suatu ukuran yang menunjukkan bagaimana masyarakat dapat memperoleh 
                    kesehatan, pendidikan, pendapatan dan lain-lain. Apabila masyarakat mendapatkan pengetahuan yang cukup dan memiliki 
                    hidup yang sehat serta standar hidup yang layak maka dapat meningkatkan Indeks Pembangunan Manusia (IPM). Setelah 
                    sempat tertekan pada tahun 2020 karena pandemi COVID-19, IPM Indonesia tahun 2021 dan 2022 mulai mengalami perbaikan. 
                    <strong><span style="color: green;">IPM Indonesia tumbuh sebesar 0,49 persen pada tahun 2021 dan 0,86 persen di tahun 2022</span></strong>, 
                    lebih tinggi dibandingkan 
                    tahun 2020 saat pandemi COVID-19 melanda Indonesia yang hanya tumbuh sebesar 0,03 persen. Pertumbuhan tahun 2022 
                    tersebut, bahkan sudah melebihi pertumbuhan sebelum masa pandemic COVID-19 di tahun 2019, yang tumbuh sebesar 0,74 persen. 
                    </p>""", unsafe_allow_html=True)

with tab3:
    st.markdown("""<style>.subheader {text-align: center;font-size: 1.3em;}</style>""", unsafe_allow_html=True)
    st.markdown("<h2 class='subheader'>Korelasi Indeks Pembangunan Manusia (IPM) dengan Prevalensi Kejadian Stunting Tahun 8-2022</h2>", unsafe_allow_html=True)

    col4 = st.container(border=True)
    with col4:      
        st.markdown("""
                    <p style="text-align: justify;">
                    Kemiskinan dan termasuk kekurangan gizi menjadi prioritas pertama dalam program 
                    <i>Sustainable Development Goals (SDGs)</i> Perserikatan Bangsa-Bangsa. Karena akan mempengaruhi 
                    tingkat kualitas manusia, yang akhirnya akan mempengaruhi produktivitas ekonomi.
                    Terjadinya kekurangan gizi dapat memengaruhi kualitas sumber daya manusia. Dimana kualitas sumber
                    daya manusia dapat diukur dengan Indeks Pembangunan Manusia (IPM). Maka dapat 
                    dikatakan dengan adanya ketidakcukupan gizi yang dapat memengaruhi kualitas sumber daya manusia, 
                    dapat memberikan dampak pada <strong><span style="color: green;">menurunnya angka IPM (Indeks Pembangunan Manusia)</span></strong>.
                    </p>""", unsafe_allow_html=True)

    # Korelasi IPM dan Stunting
    korelasi, _ = pearsonr(chart['ipm'], chart['prev_stunting'])

    ipm_scatter = alt.Chart(chart).mark_circle().encode(
        x=alt.X('ipm:Q', title='Indeks Pembangunan Manusia (IPM)'),
        y=alt.Y('prev_stunting:Q', title='Prevalensi Stunting'),
        )

    nilai_korelasi = round(korelasi,3)

    nilai_korelasi1 = alt.Chart(pd.DataFrame({'correlation': [nilai_korelasi]})).mark_text(
        align='left', baseline='middle', dx=5, color='white', fontSize=20).encode(
        text='correlation:Q'
    )

    label_korelasi = alt.Chart(pd.DataFrame({'label': ['Koefisien Korelasi']})).mark_text(
        align='left', baseline='middle', dx=-10,  dy=20, color='white', fontSize=12, ).encode(
        text='label:N'
    )
    chart_korelasi = ipm_scatter + nilai_korelasi1 + label_korelasi
    st.altair_chart(chart_korelasi , use_container_width=True)

    col5 = st.container(border=True)
    with col5:
        st.markdown("""
                    <p style="text-align: justify;">
                    Indeks Pembangunan Manusia (IPM) mengukur capaian pembangunan manusia berbasis sejumlah komponen dasar kualitas 
                    hidup salah satunya kesehatan. Studi mengenai hubungan IPM dengan kekurangan gizi pada anak juga dilakukan oleh 
                    Soheylizad M, dkk. (2016) dimana dari studi tersebut ditemukan bahwa suatu daerah yang memiliki angka IPM rendah 
                    cenderung memiliki angka prevalensi stunting yang tinggi. Studi lain menyebutkan (Anam dan Saputra 2021) IPM memiliki 
                    pengaruh negatif terhadap stunting, dimana hal tersebut menunjukkan bahwa apabila IPM meningkat maka angka prevalensi 
                    stunting menurun. Pernyataan ini sesuai dengan hasil analisa korelasi IPM dengan prevalensi kejadian stunting tahun 
                    2018 - 2022 dimana <strong><span style="color: green;">nilai koefisien korelasi bernilai -0,283 yang 
                    menunjukan IPM memiliki pengaruh negative terhadap prevalensi kejadian stunting</span></strong>
                    . Namun, pengaruhnya memiliki signifikan yang rendah, hal tersebut dikarenakan terdapat 
                    faktor lain yang dapat mempengaruhi IPM dan prevalensi kejadian penyakit.
                    </p>""", unsafe_allow_html=True)

with tab4:
    # Judul Contener
    custom_container = st.container(border=True)
    with custom_container:
        st.markdown("""<div style="font-size: 19px; font-weight: bold;">Dataset Indeks Pembangunan Manusia (IPM) dan Prevalensi Kejadian
                    Stunting Tahun <span style="color: green;">{}</span>
        """.format(pilih_tahun), unsafe_allow_html=True)
    
    final_data = filter_tahun[(filter_tahun['tahun'] == pilih_tahun)]
    st.write(final_data)

    st.markdown("""
        Sumber Data:
        1. [Ditjen Bina Pembangunan Daerah - Kementerian Dalam Negeri](https://aksi.bangda.kemendagri.go.id/emonev/DashPrev/index/2)
        2. [Badan Pusat Statistik](https://www.bps.go.id/id/publication/2023/05/16/ef80bec78ab91cb5b703b943/indeks-pembangunan-manusia-2022.html)
        """)

with tab5:
    st.markdown("""
        Referensi:
        1. Badan Pusat Statistik Indonesia. (2024, Februari 25). _Profil Kemiskinan di Indonesia Maret 2023_. Berita Resmi Statistik. _https://www.bps.go.id/id/pressrelease/2023/07/17/2016/profil-kemiskinan-di-indonesia-maret-2023.html_
        2. Fadhilah, A.E dkk.(2022). _Analisis Pengaruh Prevalensi Stunting, Kemiskinan, dan Peran Asi Ekslusif Terhadap Indeks Pembangunan Manusia di Indonesia_.Prosiding Seminar Nasional Program Studi Ilmu Pemerintahan Universitas Galuh. http://repository.unigal.ac.id/bitstream/handle/123456789/1201/Prosiding%20Seminar%20Nasional%20Program%20Studi%20Ilmu%20Pemerintahan_Ebook-34-39.pdf?sequence=1&isAllowed=y
        3. Nasrun, M. Ali dan Rahmania.(2018). _Hubungan Indikator Keberhasilan Pembangunan Ekonomi Dengan Stunting di Indonesia_. Prosiding SATIESP. Universitas Tanjungpura
        4. Nurahadiyatika, Faraiesa dkk.(2022). _Peningkatan Ketahanan Pangan dan Pengentasan Status Kemiskinan Dalam Konvergensi Penurunan Angka Stunting_. Media Gizi Indonesia (National Nutrition Journal).2022.SP(1):215-220. _https://doi.org/10.20473/mgi.v17i1SP.215–220_
        """)