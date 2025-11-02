# 🔊 SmartAudioLabReport

**License:** [Apache License 2.0](LICENSE) | [![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**Görme Engelliler için Klinik Sesli Sonuç Yorumlama Sistemi**

SmartAudioLabReport, laboratuvar raporlarını PDF formatından okuyup analiz eden ve sonuçları sesli olarak yorumlayan bir erişilebilirlik aracıdır. Sistem, laboratuvar sonuçlarını referans aralıklarıyla karşılaştırarak anlaşılır Türkçe özetler üretir.

## ⚠️ ÖNEMLİ UYARI

**Bu proje tıbbi karar verme amacıyla kullanılmamalıdır. Sadece bilgilendirme ve erişilebilirlik içindir. Tüm sağlık kararları için mutlaka bir doktora danışın.**

## 🎯 Özellikler

- 📄 **PDF Rapor Okuma**: Laboratuvar raporlarını PDF formatından otomatik olarak okur ve test sonuçlarını çıkarır
- 🔬 **Otomatik Analiz**: Test sonuçlarını referans aralıklarıyla karşılaştırarak normal/anormal durumları tespit eder
- 📝 **Akıllı Özetleme**: Kural tabanlı ve NLP tabanlı (v0.2+) özet üretimi
- 🔊 **Sesli Yorumlama**: Sonuçları Türkçe sesli olarak okur
- 🌐 **Web Arayüzü**: Streamlit tabanlı kullanıcı dostu arayüz (v0.3+)
- 👥 **Cinsiyet Özel Referanslar**: Cinsiyet bilgisine göre doğru referans aralıklarını kullanır

## 📋 Versiyon Geçmişi

| Versiyon | Özellikler |
|----------|-----------|
| **v0.1** | PDF okuma + kural tabanlı yorumlama + seslendirme |
| **v0.2** | NLP tabanlı metin özetleme eklentisi |
| **v0.3** | Web arayüzü (Streamlit) |
| **v1.0** | Çok dilli destek + model ince ayarları + ses profili seçimi (planlanan) |

## 🚀 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- pip paket yöneticisi

### Adımlar

1. **Depoyu klonlayın:**
```bash
git clone https://github.com/ladyengineersena/smart-audio-lab-report.git
cd smart-audio-lab-report
```

2. **Sanal ortam oluşturun (önerilir):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Uygulamayı başlatın:**
```bash
streamlit run app.py
```

Tarayıcınızda otomatik olarak açılacaktır (genellikle `http://localhost:8501`).

## 📁 Proje Yapısı

```
SmartAudioLabReport/
│
├── data/
│   ├── sample_reports/        # Örnek raporlar (opsiyonel)
│   └── reference_ranges.json  # Referans aralıkları
│
├── src/
│   ├── parse_report.py        # PDF okuma ve ayrıştırma
│   ├── analyze_results.py     # Sonuç analizi
│   ├── generate_summary.py    # Özet üretimi
│   └── text_to_speech.py      # Ses sentezi
│
├── app.py                     # Streamlit web arayüzü
├── requirements.txt           # Python bağımlılıkları
├── README.md                  # Bu dosya
└── LICENSE                    # Apache 2.0 lisansı
```

## 🎮 Kullanım

### Web Arayüzü (Önerilen)

1. Uygulamayı başlatın: `streamlit run app.py`
2. Tarayıcıda açılan sayfada:
   - "Rapor Yükle" sekmesinden PDF dosyanızı yükleyin
   - Cinsiyet bilgisi seçin (opsiyonel)
   - "Sonuçlar" sekmesinde analizi görüntüleyin
   - "Sesli Dinle" sekmesinde sonuçları dinleyin veya indirin

### Komut Satırı (CLI - Geliştirilme aşamasında)

```python
from src.parse_report import ReportParser
from src.analyze_results import ResultAnalyzer
from src.generate_summary import SummaryGenerator
from src.text_to_speech import TextToSpeech

# Raporu oku
parser = ReportParser()
parsed = parser.parse('rapor.pdf')

# Analiz et
analyzer = ResultAnalyzer()
analyses = analyzer.analyze(parsed['results'], gender='Erkek')

# Özet oluştur
generator = SummaryGenerator()
summary = generator.generate(analyses)

# Seslendir
tts = TextToSpeech(engine='pyttsx3', language='tr')
tts.speak(summary['audio_text'])
```

## 🔧 Yapılandırma

### Referans Aralıkları

`data/reference_ranges.json` dosyasından referans aralıklarını düzenleyebilirsiniz. Dosya şu formatta:

```json
{
  "test_name": {
    "min": 0,
    "max": 100,
    "unit": "mg/dL",
    "gender_specific": false
  }
}
```

### Ses Motoru Seçimi

- **pyttsx3**: Offline çalışır, internet gerektirmez (varsayılan)
- **gTTS**: Online çalışır, daha doğal ses kalitesi

## 🤝 Katkıda Bulunma

Katkılarınız memnuniyetle karşılanır! Lütfen:

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje **Apache License 2.0** altında lisanslanmıştır.

Detaylar için [LICENSE](LICENSE) dosyasına bakın veya [Apache 2.0 Lisans metnini](https://www.apache.org/licenses/LICENSE-2.0) inceleyin.

**Apache 2.0 Özellikleri:**
- ✅ Yeniden kullanım serbest
- ✅ Ticari kullanım serbest
- ✅ Katkı serbest
- ✅ Açık kaynak zorunluluğu yok
- ✅ Patent kullanımı serbest

## 📧 İletişim

Sorularınız veya önerileriniz için issue açabilirsiniz.

## 🙏 Teşekkürler

- PyPDF2 ve pdfminer.six - PDF işleme
- pyttsx3 ve gTTS - Ses sentezi
- Streamlit - Web arayüzü
- Hugging Face Transformers - NLP özellikleri

---

**Not:** Bu proje akademik/erişilebilirlik amaçlıdır ve tıbbi tanı/tedavi için kullanılmamalıdır.

