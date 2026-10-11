import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Sayfa Yapılandırması (Karanlık & Kurumsal Geniş Ekran)
st.set_page_config(
    page_title="TÜBİTAK 2209-A | Kolorektal Kanser Klinik Risk Analitiği",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kurumsal CSS & Cam Efekti (Glassmorphism)
st.markdown("""
    <style>
    .main { background-color: #0b0f17; }
    div[data-testid="stMetricValue"] { font-size: 1.95rem; font-weight: 800; color: #ffffff; }
    .badge-card {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(24, 24, 27, 0.6) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        margin-bottom: 22px;
    }
    .insight-card {
        background: rgba(24, 24, 27, 0.7);
        border: 1px solid #27272a;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Veri Yükleme ve Önbellekleme
@st.cache_data
def load_data():
    file_path = "TUBITAK_2209A_Kolorektal_Risk_Veri_Seti_TR.xlsx"
    df = pd.read_excel(file_path)
    
    # Resmi Türkçe Etiketler
    df['cinsiyet_label'] = df['cinsiyet_kodu'].map({1: 'Erkek', 0: 'Kadın'})
    df['sigara_label'] = df['sigara_kodu'].map({1: 'Kullanıyor', 0: 'Kullanmıyor'})
    df['alkol_label'] = df['alkol_kodu'].map({1: 'Kullanıyor', 0: 'Kullanmıyor'})
    df['aile_oykusu_label'] = df['aile_oykusu_kodu'].map({1: 'Var', 0: 'Yok'})
    df['ibh_label'] = df['ibh_kodu'].map({1: 'Var', 0: 'Yok'})
    
    risk_map = {
        'Dusuk Risk': 'Düşük Risk',
        'Orta Risk': 'Orta Risk',
        'Yuksek Risk': 'Yüksek Risk'
    }
    df['risk_kategorisi_tr'] = df['risk_kategorisi'].map(risk_map)
    return df

df = load_data()

# 2. Sol Filtre Paneli (Sidebar)
st.sidebar.markdown("""
<div class="badge-card">
    <div style="font-size: 0.8rem; font-weight: 800; color: #ef4444; letter-spacing: 0.12em;">TÜBİTAK 2209-A PROJESİ</div>
    <div style="font-size: 1.1rem; font-weight: 850; color: #ffffff; margin-top: 4px;">Klinik Karar Destek</div>
    <div style="font-size: 0.8rem; color: #a1a1aa; margin-top: 2px;">Veri Keşif & Analitik Paneli</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.subheader("Kohort Filtreleri")

min_age, max_age = int(df['yas'].min()), int(df['yas'].max())
selected_age = st.sidebar.slider("Hasta Yaş Aralığı:", min_age, max_age, (35, 85))

cinsiyet_filter = st.sidebar.multiselect(
    "Cinsiyet Dağılımı:",
    options=['Erkek', 'Kadın'],
    default=['Erkek', 'Kadın']
)

sigara_filter = st.sidebar.multiselect(
    "Tütün / Sigara Kullanımı:",
    options=['Kullanıyor', 'Kullanmıyor'],
    default=['Kullanıyor', 'Kullanmıyor']
)

aile_filter = st.sidebar.multiselect(
    "Ailede Kolorektal Öykü:",
    options=['Var', 'Yok'],
    default=['Var', 'Yok']
)

# Filtre Uygulama
filtered_df = df[
    (df['yas'] >= selected_age[0]) & (df['yas'] <= selected_age[1]) &
    (df['cinsiyet_label'].isin(cinsiyet_filter)) &
    (df['sigara_label'].isin(sigara_filter)) &
    (df['aile_oykusu_label'].isin(aile_filter))
]

# 3. Başlık Alanı
st.title("🔬 Kolorektal Kanser Klinik Risk Analitiği & Karar Destek Paneli")
st.markdown("""
Bu analitik sistem, **TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri** kapsamında yürütülen klinik modelleme sürecinde **167.497 hasta kaydının** semptom, yaşam tarzı ve erken evre risk ilişkilerini ortaya koymak amacıyla geliştirilmiştir.
""")

st.write("---")

# 4. Üst Temel Metrikler (KPIs)
col1, col2, col3, col4 = st.columns(4)

total_count = len(filtered_df)
avg_age = filtered_df['yas'].mean() if total_count > 0 else 0
high_risk_pct = (filtered_df['risk_kategorisi_tr'] == 'Yüksek Risk').mean() * 100 if total_count > 0 else 0
avg_score = filtered_df['hesaplanan_risk_skoru'].mean() if total_count > 0 else 0

with col1:
    st.metric("İncelenen Hasta Kohortu", f"{total_count:,} Hasta")
with col2:
    st.metric("Örneklem Yaş Ortalaması", f"{avg_age:.1f}")
with col3:
    st.metric("Yüksek Risk Prevalansı", f"%{high_risk_pct:.1f}")
with col4:
    st.metric("Ortalama Risk Skoru", f"{avg_score:.1f} / 100")

st.write("---")

# 5. Profesyonel Sekme (Tab) Mimarisi
tab1, tab2, tab3 = st.tabs([
    "📈 Genel Dağılım & Yaş Analizi", 
    "🧬 Klinik & Yaşam Tarzı Risk Faktörleri", 
    "🔥 İstatistiksel Korelasyon & Veri İnceleme"
])

# SEKME 1: GENEL DAĞILIM
with tab1:
    col_left, col_right = st.columns([1.3, 1])
    
    with col_left:
        st.subheader("Yaş Gruplarına Göre Ortalama Risk Seyri")
        
        # Yaş bazında ortalama risk tablosu
        age_grouped = filtered_df.groupby(['yas', 'risk_kategorisi_tr'])['hesaplanan_risk_skoru'].mean().reset_index()
        
        fig_age = px.bar(
            age_grouped,
            x="yas",
            y="hesaplanan_risk_skoru",
            color="risk_kategorisi_tr",
            barmode="overlay",
            color_discrete_map={"Düşük Risk": "#22c55e", "Orta Risk": "#eab308", "Yüksek Risk": "#ef4444"},
            template="plotly_dark"
        )
        
        # ÖZEL VE TERTEMİZ TÜRKÇE TOOLTIP (avg of veya çirkin yazılar tamamen kalktı)
        fig_age.update_traces(
            hovertemplate="<b>Hasta Yaşı:</b> %{x}<br><b>Ortalama Risk Skoru:</b> %{y:.1f} / 100<extra></extra>"
        )
        fig_age.update_layout(
            xaxis_title="Hasta Yaşı",
            yaxis_title="Ortalama Risk Skoru",
            legend_title="Risk Düzeyi",
            height=390,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_age, use_container_width=True)

    with col_right:
        st.subheader("Kohort Risk Dağılım Oranı")
        risk_counts = filtered_df['risk_kategorisi_tr'].value_counts().reset_index()
        risk_counts.columns = ['Risk Düzeyi', 'Hasta Sayısı']
        
        fig_pie = px.pie(
            risk_counts,
            names="Risk Düzeyi",
            values="Hasta Sayısı",
            color="Risk Düzeyi",
            color_discrete_map={"Düşük Risk": "#22c55e", "Orta Risk": "#eab308", "Yüksek Risk": "#ef4444"},
            hole=0.48,
            template="plotly_dark"
        )
        fig_pie.update_traces(
            hovertemplate="<b>%{label}</b><br>Kayıt Sayısı: %{value:,}<br>Oran: %{percent}<extra></extra>"
        )
        fig_pie.update_layout(height=390, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("""
    <div class="insight-card">
        <h4 style="margin: 0 0 8px 0; color: #ffffff;">📋Araştırmacı Notu:</h4>
        <span style="color: #a1a1aa; font-size: 0.95rem; line-height: 1.6;">
        Kohort analizinde 50 yaş üzerindeki bireylerde klinik risk eğrisinin belirgin şekilde yükseldiği gözlemlenmektedir. Erken uyarı modellerinin özellikle 50-75 yaş aralığında tarama programlarıyla desteklenmesi kritik önem taşımaktadır.
        </span>
    </div>
    """, unsafe_allow_html=True)

# SEKME 2: FAKTÖRLER
with tab2:
    st.subheader("Yaşam Tarzı ve Kronik Öykünün Yüksek Riske Etkisi")
    
    factors = {
        "Sigara": filtered_df.groupby('sigara_label')['hedef_yuksek_risk'].mean() * 100,
        "Alkol": filtered_df.groupby('alkol_label')['hedef_yuksek_risk'].mean() * 100,
        "Aile Öyküsü": filtered_df.groupby('aile_oykusu_label')['hedef_yuksek_risk'].mean() * 100,
        "İBH Öyküsü": filtered_df.groupby('ibh_label')['hedef_yuksek_risk'].mean() * 100
    }
    
    comp_data = []
    for f_name, series in factors.items():
        for status, val in series.items():
            comp_data.append({"Klinik Faktör": f"{f_name} ({status})", "Yüksek Risk Oranı (%)": val})
            
    comp_df = pd.DataFrame(comp_data)
    
    fig_bar = px.bar(
        comp_df,
        x="Klinik Faktör",
        y="Yüksek Risk Oranı (%)",
        color="Yüksek Risk Oranı (%)",
        color_continuous_scale="Reds",
        template="plotly_dark"
    )
    fig_bar.update_traces(
        hovertemplate="<b>%{x}</b><br>Yüksek Risk Oranı: %%%{y:.1f}<extra></extra>"
    )
    fig_bar.update_layout(
        xaxis_title="Klinik Parametre ve Durum",
        yaxis_title="Yüksek Risk Oranı (%)",
        height=400,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# SEKME 3: KORELASYON & TABLO
with tab3:
    c_cor, c_table = st.columns([1.1, 1])
    
    with c_cor:
        st.subheader("Klinik Değişkenler Arası Bağıntı Matrisi")
        
        corr_df = filtered_df[[
            'yas', 'aile_oykusu_kodu', 'sigara_kodu', 'alkol_kodu', 
            'diyabet_kodu', 'ibh_kodu', 'vki_skoru', 'hesaplanan_risk_skoru'
        ]].rename(columns={
            'yas': 'Yaş',
            'aile_oykusu_kodu': 'Aile Öyküsü',
            'sigara_kodu': 'Sigara',
            'alkol_kodu': 'Alkol',
            'diyabet_kodu': 'Diyabet',
            'ibh_kodu': 'İBH',
            'vki_skoru': 'VKİ',
            'hesaplanan_risk_skoru': 'Risk Skoru'
        })
        
        corr = corr_df.corr()
        
        fig_corr = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            aspect="auto",
            template="plotly_dark"
        )
        # ÖZEL KORELASYON TOOLTIP (color: 1 yazısı tamamen kalktı)
        fig_corr.update_traces(
            hovertemplate="<b>Değişken 1:</b> %{x}<br><b>Değişken 2:</b> %{y}<br><b>Korelasyon Katsayısı (r):</b> %{z:.2f}<extra></extra>"
        )
        fig_corr.update_layout(height=420, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_corr, use_container_width=True)

    with c_table:
        st.subheader("Kohort Örneklem Veri Tablosu")
        st.dataframe(
            filtered_df[['yas', 'cinsiyet_label', 'sigara_label', 'alkol_label', 'aile_oykusu_label', 'hesaplanan_risk_skoru', 'risk_kategorisi_tr']].head(100),
            column_config={
                "yas": "Yaş",
                "cinsiyet_label": "Cinsiyet",
                "sigara_label": "Sigara",
                "alkol_label": "Alkol",
                "aile_oykusu_label": "Aile Öyküsü",
                "hesaplanan_risk_skoru": st.column_config.ProgressColumn(
                    "Risk Skoru", format="%.1f", min_value=0, max_value=100
                ),
                "risk_kategorisi_tr": "Kategori"
            },
            hide_index=True,
            height=420,
            use_container_width=True
        )

# Dipnot & İmzalar
st.write("---")
st.caption("Veri Seti: TÜBİTAK 2209-A Klinik Karar Destek Araştırma Kapsamı | Araştırmacı & Geliştirici: Halil Umut Koç (Muğla Sıtkı Koçman Üniversitesi - YBS)")