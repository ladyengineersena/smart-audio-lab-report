"""
Metin-ses dönüştürme modülü.
"""
import pyttsx3
import gtts
from typing import Optional
import io


class TextToSpeech:
    """Metni sese dönüştürür."""
    
    def __init__(self, engine: str = 'pyttsx3', language: str = 'tr'):
        """
        Args:
            engine: 'pyttsx3' (offline) veya 'gtts' (online)
            language: Dil kodu ('tr', 'en', vb.)
        """
        self.engine_type = engine
        self.language = language
        self.engine = None
        
        if engine == 'pyttsx3':
            try:
                self.engine = pyttsx3.init()
                self._configure_pyttsx3()
            except Exception as e:
                print(f"pyttsx3 yüklenemedi: {e}")
                self.engine = None
        elif engine == 'gtts':
            # gTTS için engine gerekmez, direkt kullanılır
            pass
    
    def _configure_pyttsx3(self):
        """pyttsx3 ayarlarını yapılandırır."""
        if self.engine:
            # Hız ayarı (kelime/dakika)
            rate = self.engine.getProperty('rate')
            self.engine.setProperty('rate', 150)
            
            # Ses seviyesi (0.0-1.0)
            self.engine.setProperty('volume', 1.0)
            
            # Türkçe ses seçimi (mevcut sistem sesleri)
            voices = self.engine.getProperty('voices')
            # Türkçe ses varsa seç
            for voice in voices:
                if 'turkish' in voice.name.lower() or 'tr' in voice.id.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
    
    def speak(self, text: str) -> bool:
        """Metni seslendirir (offline - pyttsx3)."""
        if self.engine_type == 'pyttsx3' and self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
                return True
            except Exception as e:
                print(f"Seslendirme hatası: {e}")
                return False
        return False
    
    def save_to_file(self, text: str, output_path: str) -> bool:
        """Metni ses dosyasına kaydeder."""
        if self.engine_type == 'pyttsx3' and self.engine:
            try:
                self.engine.save_to_file(text, output_path)
                self.engine.runAndWait()
                return True
            except Exception as e:
                print(f"Dosyaya kaydetme hatası: {e}")
                return False
        
        elif self.engine_type == 'gtts':
            try:
                tts = gtts.gTTS(text=text, lang=self.language, slow=False)
                tts.save(output_path)
                return True
            except Exception as e:
                print(f"gTTS kaydetme hatası: {e}")
                return False
        
        return False
    
    def get_audio_bytes(self, text: str) -> Optional[bytes]:
        """Metni ses byte'larına dönüştürür (gTTS için)."""
        if self.engine_type == 'gtts':
            try:
                tts = gtts.gTTS(text=text, lang=self.language, slow=False)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                return audio_buffer.read()
            except Exception as e:
                print(f"gTTS byte dönüştürme hatası: {e}")
                return None
        return None
    
    def set_voice_profile(self, profile: str):
        """Ses profili ayarlar (v1.0 özelliği)."""
        if self.engine_type == 'pyttsx3' and self.engine:
            voices = self.engine.getProperty('voices')
            if profile == 'female':
                # Kadın sesi seç
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
            elif profile == 'male':
                # Erkek sesi seç
                for voice in voices:
                    if 'male' in voice.name.lower() and 'female' not in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break

