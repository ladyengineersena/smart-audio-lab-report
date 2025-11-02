"""
SmartAudioLabReport - Web Arayüzü
Streamlit tabanlı görme engelliler için laboratuvar raporu okuma sistemi.
"""
import streamlit as st
import sys
from pathlib import Path

# Proje yollarını ekle
project_root = Path(__file__).parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

from parse_report import ReportParser
from analyze_results import ResultAnalyzer
from generate_summary import SummaryGenerator
from text_to_speech import TextToSpeech

# Sayfa yapılandırması
st.set_page_config(
    page_title="SmartAudioLabReport",
    page_icon="🔊",
    layout="wide"
)

# Başlık ve açıklama
st.title("🔊 SmartAudioLabReport")
st.markdown("**Görme Engelliler için Klinik Sesli Sonuç Yorumlama Sistemi**")
st.markdown("---")

# Yan panel - Ayarlar
with st.sidebar:
    st.header("⚙️ Ayarlar")
    
    gender = st.selectbox(
        "Cinsiyet",
        ["Belirtilmemiş", "Erkek", "Kadın"],
        help="Cinsiyet bilgisi referans aralıklarını belirlemede kullanılır."
    )
    
    use_nlp = st.checkbox(
        "NLP Özetleme Kullan",
        value=False,
        help="v0.2 özelliği: Gelişmiş NLP tabanlı özetleme."
    )
    
    tts_engine = st.selectbox(
        "Ses Motoru",
        ["pyttsx3", "gtts"],
        help="pyttsx3: Offline, gtts: Online (internet gerekli)"
    )
    
    st.markdown("---")
    st.markdown("### 📋 Versiyon Bilgisi")
    st.info("**v0.3** - Web Arayüzü\n\n**Özellikler:**\n- PDF okuma\n- Otomatik analiz\n- Sesli yorumlama")

# Ana içerik
tab1, tab2, tab3 = st.tabs(["📄 Rapor Yükle", "📊 Sonuçlar", "🔊 Sesli Dinle"])

with tab1:
    st.header("Laboratuvar Raporu Yükle")
    
    uploaded_file = st.file_uploader(
        "PDF rapor dosyası seçin",
        type=['pdf'],
        help="Laboratuvar sonuçlarınızın PDF formatındaki dosyasını yükleyin."
    )
    
    if uploaded_file is not None:
        # Dosyayı geçici olarak kaydet
        temp_path = project_root / 'temp_report.pdf'
        with open(temp_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # Raporu parse et
        with st.spinner('Rapor okunuyor...'):
            parser = ReportParser()
            parsed_data = parser.parse(str(temp_path))
        
        if 'error' not in parsed_data:
            st.success(f"✓ Rapor başarıyla okundu. {parsed_data.get('test_count', 0)} test bulundu.")
            
            # Session state'e kaydet
            st.session_state['parsed_data'] = parsed_data
            st.session_state['uploaded'] = True
            
            # Analiz yap
            with st.spinner('Sonuçlar analiz ediliyor...'):
                analyzer = ResultAnalyzer()
                gender_val = None if gender == "Belirtilmemiş" else gender
                analyses = analyzer.analyze(parsed_data['results'], gender_val)
                st.session_state['analyses'] = analyses
            
            # Özet oluştur
            with st.spinner('Özet hazırlanıyor...'):
                generator = SummaryGenerator(use_nlp=use_nlp)
                summary = generator.generate(analyses, use_nlp_summary=use_nlp)
                st.session_state['summary'] = summary
            
            st.balloons()
        else:
            st.error("Rapor okunamadı. Lütfen geçerli bir PDF dosyası yükleyin.")

with tab2:
    st.header("Analiz Sonuçları")
    
    if 'analyses' in st.session_state:
        analyses = st.session_state['analyses']
        summary = st.session_state.get('summary', {})
        
        # Özet istatistikler
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Toplam Test",
                analyses['summary']['total_tests']
            )
        
        with col2:
            st.metric(
                "Normal Sonuç",
                analyses['summary']['normal_count'],
                delta=None,
                delta_color="normal"
            )
        
        with col3:
            st.metric(
                "Anormal Sonuç",
                analyses['summary']['abnormal_count'],
                delta=None,
                delta_color="inverse"
            )
        
        st.markdown("---")
        
        # Basit özet
        st.subheader("📝 Özet")
        st.info(summary.get('simple_summary', 'Özet oluşturulamadı.'))
        
        # Detaylı yorumlama
        with st.expander("📋 Detaylı Yorumlama"):
            st.text(summary.get('detailed_commentary', ''))
        
        # NLP özeti (varsa)
        if summary.get('nlp_summary'):
            with st.expander("🤖 NLP Özeti"):
                st.info(summary['nlp_summary'])
        
        # Test sonuçları tablosu
        st.markdown("---")
        st.subheader("🔬 Test Sonuçları")
        
        import pandas as pd
        
        results_data = []
        for test_name, analysis in analyses['analyses'].items():
            results_data.append({
                'Test': test_name.upper(),
                'Değer': f"{analysis['value']} {analysis.get('unit', '')}",
                'Durum': analysis['status'],
                'Referans': analysis.get('reference_range', '')
            })
        
        if results_data:
            df = pd.DataFrame(results_data)
            st.dataframe(df, use_container_width=True)
    else:
        st.info("👈 Lütfen önce bir rapor yükleyin.")

with tab3:
    st.header("🔊 Sesli Dinleme")
    
    if 'summary' in st.session_state:
        summary = st.session_state['summary']
        audio_text = summary.get('audio_text', '')
        
        if audio_text:
            st.subheader("Seslendirilecek Metin")
            st.text_area("", audio_text, height=200, disabled=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("▶️ Canlı Dinle (Tarayıcı)", use_container_width=True):
                    with st.spinner('Ses üretiliyor...'):
                        tts = TextToSpeech(engine=tts_engine, language='tr')
                        if tts_engine == 'gtts':
                            # gTTS için MP3 oluştur
                            audio_file = project_root / 'temp_audio.mp3'
                            if tts.save_to_file(audio_text, str(audio_file)):
                                st.audio(str(audio_file), format='audio/mp3')
                        else:
                            # pyttsx3 için canlı okuma (tarayıcıda çalışmaz, bilgi ver)
                            st.info("pyttsx3 tarayıcıda canlı çalışmaz. Lütfen indirip dinleyin.")
            
            with col2:
                if st.button("💾 Ses Dosyası İndir", use_container_width=True):
                    with st.spinner('Dosya oluşturuluyor...'):
                        tts = TextToSpeech(engine=tts_engine, language='tr')
                        audio_file = project_root / 'lab_report_audio.mp3'
                        if tts.save_to_file(audio_text, str(audio_file)):
                            with open(audio_file, 'rb') as f:
                                st.download_button(
                                    label="📥 MP3 İndir",
                                    data=f.read(),
                                    file_name='lab_report_audio.mp3',
                                    mime='audio/mpeg'
                                )
        else:
            st.warning("Seslendirilecek metin bulunamadı.")
    else:
        st.info("👈 Lütfen önce bir rapor yükleyin.")

# Alt bilgi
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p><strong>⚠️ ÖNEMLİ UYARI:</strong> Bu proje tıbbi karar verme amacıyla kullanılmamalıdır. 
    Sadece bilgilendirme ve erişilebilirlik içindir. Tüm sağlık kararları için mutlaka 
    bir doktora danışın.</p>
    <p>SmartAudioLabReport v0.3 | Apache 2.0 License</p>
    </div>
    """,
    unsafe_allow_html=True
)

