"""
Rapor özeti ve yorumlama metni üretme modülü.
v0.2: NLP tabanlı özetleme desteği eklendi.
"""
from typing import Dict, Optional
try:
    from transformers import pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    torch = None


class SummaryGenerator:
    """Laboratuvar sonuçları için özet ve yorumlama metni üretir."""
    
    def __init__(self, use_nlp: bool = False):
        self.use_nlp = use_nlp
        self.summarizer = None
        
        if use_nlp:
            if not TRANSFORMERS_AVAILABLE:
                print("Transformers kütüphanesi yüklü değil. NLP özetleme kullanılamıyor.")
                self.use_nlp = False
                return
            try:
                self.summarizer = pipeline(
                    "summarization",
                    model="facebook/bart-large-cnn",
                    device=0 if torch.cuda.is_available() else -1
                )
            except Exception as e:
                print(f"NLP modeli yüklenemedi, kural tabanlı mod kullanılıyor: {e}")
                self.use_nlp = False
    
    def generate_simple_summary(self, analyses: Dict) -> str:
        """Kural tabanlı basit özet üretir."""
        summary_parts = []
        summary_data = analyses.get('summary', {})
        
        total = summary_data.get('total_tests', 0)
        normal = summary_data.get('normal_count', 0)
        abnormal = summary_data.get('abnormal_count', 0)
        
        summary_parts.append(f"Laboratuvar sonuçlarınız analiz edildi. Toplam {total} test değerlendirildi.")
        
        if normal > 0:
            summary_parts.append(f"{normal} test sonucu normal aralıkta.")
        
        if abnormal > 0:
            summary_parts.append(f"{abnormal} test sonucu referans aralığının dışında.")
        
        # Anormal sonuçları listele
        abnormal_results = []
        for test_name, analysis in analyses.get('analyses', {}).items():
            if analysis.get('is_normal') is False:
                abnormal_results.append(analysis.get('message', ''))
        
        if abnormal_results:
            summary_parts.append("\nDikkat gereken sonuçlar:")
            for result in abnormal_results:
                summary_parts.append(f"- {result}")
        
        # Normal sonuçlar için kısa özet
        normal_count = 0
        for test_name, analysis in analyses.get('analyses', {}).items():
            if analysis.get('is_normal') is True:
                normal_count += 1
        
        if normal_count == total and total > 0:
            summary_parts.append("\nTüm test sonuçlarınız normal aralıkta. Genel sağlık durumunuz iyi görünüyor.")
        
        return "\n".join(summary_parts)
    
    def generate_detailed_commentary(self, analyses: Dict) -> str:
        """Detaylı yorumlama metni üretir."""
        commentary = []
        commentary.append("=" * 50)
        commentary.append("DETAYLI LABORATUVAR SONUÇ YORUMU")
        commentary.append("=" * 50)
        commentary.append("")
        
        # Testleri kategorilere ayır
        hematology_tests = ['hemoglobin', 'hematocrit', 'wbc', 'rbc', 'platelet']
        biochemistry_tests = ['glucose', 'cholesterol', 'triglyceride', 'creatinine', 'alt', 'ast']
        
        hematology_results = []
        biochemistry_results = []
        
        for test_name, analysis in analyses.get('analyses', {}).items():
            test_entry = {
                'name': analysis.get('message', test_name),
                'value': analysis.get('value'),
                'unit': analysis.get('unit', ''),
                'status': analysis.get('status', 'unknown')
            }
            
            if test_name in hematology_tests:
                hematology_results.append(test_entry)
            elif test_name in biochemistry_tests:
                biochemistry_results.append(test_entry)
        
        if hematology_results:
            commentary.append("HEMATOLOJİ (Kan Sayımı) Sonuçları:")
            commentary.append("-" * 40)
            for result in hematology_results:
                status_icon = "✓" if result['status'] == 'normal' else "⚠"
                commentary.append(f"{status_icon} {result['name']}: {result['value']} {result['unit']}")
            commentary.append("")
        
        if biochemistry_results:
            commentary.append("BİYOKİMYA Sonuçları:")
            commentary.append("-" * 40)
            for result in biochemistry_results:
                status_icon = "✓" if result['status'] == 'normal' else "⚠"
                commentary.append(f"{status_icon} {result['name']}: {result['value']} {result['unit']}")
            commentary.append("")
        
        # Genel değerlendirme
        summary = analyses.get('summary', {})
        if summary.get('abnormal_count', 0) > 0:
            commentary.append("ÖNEMLİ NOT:")
            commentary.append("Bazı test sonuçlarınız referans aralığının dışında.")
            commentary.append("Lütfen bu sonuçları doktorunuzla görüşün.")
        else:
            commentary.append("GENEL DEĞERLENDİRME:")
            commentary.append("Tüm test sonuçlarınız normal aralıkta.")
        
        return "\n".join(commentary)
    
    def generate(self, analyses: Dict, use_nlp_summary: bool = False) -> Dict:
        """Özet ve yorumlama metni üretir."""
        simple_summary = self.generate_simple_summary(analyses)
        detailed_commentary = self.generate_detailed_commentary(analyses)
        
        # NLP tabanlı özet (opsiyonel)
        nlp_summary = None
        if use_nlp_summary and self.use_nlp and self.summarizer:
            try:
                combined_text = simple_summary + "\n\n" + detailed_commentary
                nlp_result = self.summarizer(
                    combined_text,
                    max_length=150,
                    min_length=50,
                    do_sample=False
                )
                nlp_summary = nlp_result[0]['summary_text']
            except Exception as e:
                print(f"NLP özetleme hatası: {e}")
        
        return {
            'simple_summary': simple_summary,
            'detailed_commentary': detailed_commentary,
            'nlp_summary': nlp_summary,
            'audio_text': nlp_summary if nlp_summary else simple_summary
        }

