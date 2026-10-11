# 🩺 TÜBİTAK 2209-A: Kolorektal Kanser Klinik Risk Analitiği & Karar Destek Paneli

Bu depo, **TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı** kapsamında yürütülen *"Kolorektal Kanseri Hasta Danışan ve Erken Uyarı Sistemi"* başlıklı araştırma projesinin etkileşimli veri analitiği ve klinik karar destek katmanını içermektedir.

🔗 **Canlı Gösterge Paneli:** [https://klinik-risk-paneli.streamlit.app/](https://klinik-risk-paneli.streamlit.app/)  
🌐 **Geliştirici & Portfolyo:** [halilumutkoc.com](https://halilumutkoc.com)

---

## 📌 Proje Özeti & Kapsam

Kolorektal kanser vakalarında erken teşhis ve risk profillemesi hayati önem taşımaktadır. Bu çalışma çerçevesinde:
- **167.497 klinik gözlem** verisi üzerinde eksik veri temizleme, uç değer analizi ve kategorik değişken standardizasyonu gerçekleştirilmiştir.
- Yaş, cinsiyet, tütün/alkol kullanımı, genetik öykü ve kronik rahatsızlık parametreleri kohort bazında sınıflandırılmıştır.
- Hekimlerin ve araştırmacıların değişkenler arası bağıntıları keşfedebilmesi adına bulut tabanlı, etkileşimli bir klinik karar destek arayüzü kurgulanmıştır.

---

## 🚀 Temel Özellikler

- **Dinamik Kohort Filtreleme:** Demografik ve klinik parametrelere göre hasta gruplarını anlık filtreleme ve alt grup analizi.
- **Klinik Risk Matrisi & Korelasyon:** Risk faktörlerinin göreceli ağırlıklarını ve değişkenler arası korelasyonları görselleştiren dinamik Plotly grafikleri.
- **Büyük Veri Yönetimi:** 160 binden fazla gözlem üzerinde optimize edilmiş veri işleme mimarisi.
- **Bulut Tabanlı Dağıtım:** Sıfır kurulum gereksinimiyle doğrudan web üzerinden erişilebilir Streamlit Cloud entegrasyonu.

---

## 🛠️ Kullanılan Teknolojiler & Kütüphaneler

- **Dil:** Python
- **Arayüz & Web Çatısı:** Streamlit
- **Veri Manipülasyonu:** Pandas, OpenPyXL
- **İnteraktif Görselleştirme:** Plotly Express
- **Dağıtım (Deployment):** Streamlit Community Cloud

---

## 💻 Yerel Ortamda Çalıştırma (Local Setup)

Projeyi yerel makinenizde test etmek için:

```bash
# 1. Repoyu klonlayın
git clone [https://github.com/halilumutkoc/tubitak-kolorektal-dashboard.git](https://github.com/halilumutkoc/tubitak-kolorektal-dashboard.git)
cd tubitak-kolorektal-dashboard

# 2. Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# 3. Streamlit uygulamasını başlatın
streamlit run app.py
