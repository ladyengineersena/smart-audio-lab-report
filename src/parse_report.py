"""
PDF laboratuvar raporu okuma ve ayrıştırma modülü.
"""
import re
from typing import Dict, Optional
from pdfminer.high_level import extract_text


class ReportParser:
    """Laboratuvar raporlarını PDF'den okur ve yapılandırılmış veriye dönüştürür."""
    
    def __init__(self):
        self.test_patterns = {
            'hemoglobin': r'Hb|Hemoglobin',
            'hematocrit': r'Hct|Hematokrit',
            'wbc': r'WBC|Lökosit',
            'rbc': r'RBC|Eritrosit',
            'platelet': r'PLT|Trombosit',
            'glucose': r'Glukoz|Glucose|Açlık Kan Şekeri',
            'cholesterol': r'Kolesterol|Cholesterol',
            'triglyceride': r'Triglyceride|Triglisirit',
            'creatinine': r'Kreatinin|Creatinine',
            'alt': r'ALT|Alanin Aminotransferaz',
            'ast': r'AST|Aspartat Aminotransferaz',
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """PDF dosyasından metin çıkarır."""
        try:
            text = extract_text(pdf_path)
            return text
        except Exception as e:
            print(f"PDF okuma hatası: {e}")
            return ""
    
    def parse_numeric_value(self, text: str) -> Optional[float]:
        """Metinden sayısal değer çıkarır."""
        # Sayıları ve ondalık değerleri bulur
        match = re.search(r'(\d+[.,]?\d*)', text.replace(',', '.'))
        if match:
            try:
                return float(match.group(1))
            except:
                return None
        return None
    
    def find_test_results(self, text: str) -> Dict[str, Dict]:
        """Metinde test sonuçlarını bulur ve yapılandırır."""
        results = {}
        lines = text.split('\n')
        
        for line in lines:
            line_upper = line.upper()
            for test_name, pattern in self.test_patterns.items():
                if re.search(pattern, line_upper, re.IGNORECASE):
                    value = self.parse_numeric_value(line)
                    if value is not None:
                        results[test_name] = {
                            'value': value,
                            'unit': self.extract_unit(line),
                            'raw_line': line.strip()
                        }
                    break
        
        return results
    
    def extract_unit(self, text: str) -> str:
        """Metinden birim bilgisini çıkarır."""
        common_units = ['g/dL', 'mg/dL', 'mg/L', 'U/L', 'IU/L', 'mmol/L', 
                       'x10^9/L', 'x10^12/L', '%', 'fL', 'pg']
        for unit in common_units:
            if unit in text:
                return unit
        return ""
    
    def parse(self, pdf_path: str) -> Dict:
        """Ana parsing fonksiyonu."""
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return {'error': 'PDF okunamadı', 'results': {}}
        
        results = self.find_test_results(text)
        
        return {
            'raw_text': text[:500],  # İlk 500 karakter
            'results': results,
            'test_count': len(results)
        }

