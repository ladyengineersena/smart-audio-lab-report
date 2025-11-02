"""
Laboratuvar sonuçlarını referans aralıklarıyla karşılaştıran analiz modülü.
"""
import json
from typing import Dict, Optional
from pathlib import Path


class ResultAnalyzer:
    """Test sonuçlarını referans aralıklarıyla karşılaştırır ve yorumlar."""
    
    def __init__(self, reference_ranges_path: Optional[str] = None):
        if reference_ranges_path is None:
            reference_ranges_path = Path(__file__).parent.parent / 'data' / 'reference_ranges.json'
        
        self.reference_ranges = self.load_reference_ranges(reference_ranges_path)
        self.test_names_tr = {
            'hemoglobin': 'Hemoglobin',
            'hematocrit': 'Hematokrit',
            'wbc': 'Lökosit',
            'rbc': 'Eritrosit',
            'platelet': 'Trombosit',
            'glucose': 'Açlık Kan Şekeri',
            'cholesterol': 'Kolesterol',
            'triglyceride': 'Triglisirit',
            'creatinine': 'Kreatinin',
            'alt': 'ALT',
            'ast': 'AST',
        }
    
    def load_reference_ranges(self, path: Path) -> Dict:
        """Referans aralıklarını yükler."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Uyarı: {path} bulunamadı, varsayılan aralıklar kullanılıyor.")
            return self.get_default_ranges()
    
    def get_default_ranges(self) -> Dict:
        """Varsayılan referans aralıkları."""
        return {
            'hemoglobin': {'min': 12.0, 'max': 16.0, 'unit': 'g/dL', 'gender_specific': True},
            'hematocrit': {'min': 36.0, 'max': 46.0, 'unit': '%', 'gender_specific': True},
            'wbc': {'min': 4.0, 'max': 10.0, 'unit': 'x10^9/L'},
            'rbc': {'min': 4.5, 'max': 5.5, 'unit': 'x10^12/L', 'gender_specific': True},
            'platelet': {'min': 150, 'max': 400, 'unit': 'x10^9/L'},
            'glucose': {'min': 70, 'max': 100, 'unit': 'mg/dL'},
            'cholesterol': {'min': 0, 'max': 200, 'unit': 'mg/dL'},
            'triglyceride': {'min': 0, 'max': 150, 'unit': 'mg/dL'},
            'creatinine': {'min': 0.6, 'max': 1.2, 'unit': 'mg/dL', 'gender_specific': True},
            'alt': {'min': 0, 'max': 41, 'unit': 'U/L', 'gender_specific': True},
            'ast': {'min': 0, 'max': 40, 'unit': 'U/L'},
        }
    
    def check_range(self, test_name: str, value: float, gender: Optional[str] = None) -> Dict:
        """Bir test değerinin referans aralığında olup olmadığını kontrol eder."""
        if test_name not in self.reference_ranges:
            return {
                'status': 'unknown',
                'message': f'{test_name} için referans aralığı bulunamadı',
                'is_normal': None
            }
        
        ref = self.reference_ranges[test_name]
        
        # Cinsiyet özel aralık varsa kullan
        if ref.get('gender_specific') and gender:
            gender_key = 'male' if gender.lower() == 'erkek' else 'female'
            if gender_key in ref:
                ref = ref[gender_key]
        
        min_val = ref.get('min', 0)
        max_val = ref.get('max', float('inf'))
        
        is_normal = min_val <= value <= max_val
        
        if value < min_val:
            status = 'low'
            message = f'{self.test_names_tr.get(test_name, test_name)} değeri düşük (referans: {min_val}-{max_val} {ref.get("unit", "")})'
        elif value > max_val:
            status = 'high'
            message = f'{self.test_names_tr.get(test_name, test_name)} değeri yüksek (referans: {min_val}-{max_val} {ref.get("unit", "")})'
        else:
            status = 'normal'
            message = f'{self.test_names_tr.get(test_name, test_name)} değeri normal (referans: {min_val}-{max_val} {ref.get("unit", "")})'
        
        return {
            'status': status,
            'message': message,
            'is_normal': is_normal,
            'reference_range': f'{min_val}-{max_val} {ref.get("unit", "")}'
        }
    
    def analyze(self, results: Dict[str, Dict], gender: Optional[str] = None) -> Dict:
        """Tüm sonuçları analiz eder ve özet oluşturur."""
        analyses = {}
        abnormal_count = 0
        normal_count = 0
        
        for test_name, test_data in results.items():
            value = test_data.get('value')
            if value is not None:
                analysis = self.check_range(test_name, value, gender)
                analyses[test_name] = {
                    **test_data,
                    **analysis
                }
                
                if analysis['is_normal']:
                    normal_count += 1
                elif analysis['is_normal'] is False:
                    abnormal_count += 1
        
        return {
            'analyses': analyses,
            'summary': {
                'total_tests': len(analyses),
                'normal_count': normal_count,
                'abnormal_count': abnormal_count,
                'unknown_count': len(analyses) - normal_count - abnormal_count
            }
        }

