from functools import lru_cache
from typing import List
from presidio_analyzer import AnalyzerEngine, RecognizerResult, AnalyzerEngine, RecognizerRegistry

from SemanticShield.config_defaults import ConfigDefaults
from SemanticShield.dummy_data import DummyData
from SemanticShield.shield_config import PIIConfig
from SemanticShield.recognizers.canadian_passport_recognizer import CanadianPassportRecognizer
from SemanticShield.recognizers.canadian_sin_recognizer import CanadianSINRecognizer
from SemanticShield.recognizers.ontario_driver_license_recognizer import OntarioLicenseRecognizer
from SemanticShield.recognizers.ontario_health_card_recognizer import OntarioHealthCardRecognizer
from SemanticShield.recognizers.canadian_bank_acct_recognizer import CanadianBankAccountRecognizer

from SemanticShield.supported_entities import supported_entities

def init_analyzer():
    #TODO automate list of custom recognizers
    ca_passport_recognizer = CanadianPassportRecognizer()
    ca_sin_recognizer = CanadianSINRecognizer()
    ca_bank_acct_recognizer = CanadianBankAccountRecognizer()
    on_drivers_license_recognizer = OntarioLicenseRecognizer()
    on_health_card_recognizer = OntarioHealthCardRecognizer()
    registry = RecognizerRegistry()
    registry.load_predefined_recognizers()
    registry.add_recognizer(ca_passport_recognizer)
    registry.add_recognizer(ca_sin_recognizer)
    registry.add_recognizer(ca_bank_acct_recognizer)
    registry.add_recognizer(on_drivers_license_recognizer)
    registry.add_recognizer(on_health_card_recognizer)
    return AnalyzerEngine(registry=registry)

analyzer_instace = init_analyzer()

class PIIAnalyzer:
    def __init__(self, config: PIIConfig=PIIConfig(**ConfigDefaults.pii) ) -> None:
        global analyzer_instace
        self.analyzer = analyzer_instace
        
        self.dummy_data = DummyData(config.operation, config.redact_string)
        self.config = config

    def filter_permissive(self, result_list: List[RecognizerResult]) -> List[RecognizerResult]:
        if self.config.permissive:
            result_list = list(filter(lambda x: x.entity_type not in self.config.permissive_allow, result_list))
        return result_list

    def select_longest_overlapping_entries(self, entries):
        entries.sort(key=lambda x: (x.start, -x.end))  # Sort by start in ascending order and end in descending order
        
        result = []
        current_entry = None
        
        for entry in entries:
            if current_entry is None or entry.start > current_entry.end:
                result.append(entry)
                current_entry = entry
            elif entry.end > current_entry.end:
                current_entry = entry
        
        return result

    def get_supported_entities(self):
        entities = self.analyzer.get_supported_entities()
        for e in entities:
            if e not in supported_entities.keys():
                supported_entities[e] = 'Other'
        return supported_entities
    
    @lru_cache
    def analyze(self, text: str) -> List[RecognizerResult]:
        results = self.analyzer.analyze(text=text,
                                entities=None,
                                language='en')
        results = self.filter_permissive(results)
        results = self.select_longest_overlapping_entries(results)
        results.sort(key=lambda x: (x.start, x.score), reverse=True)
        #remove duplicates, keep highest score
        unique_list = []
        if len(results) > 0:
            unique_list.append(results[0])
            for index in range(1,len(results)):
                previous = results[index-1]
                current = results[index]
                if previous.start != current.start and previous.end != current.end:
                    unique_list.append(current)
        return unique_list
    
    def score(self, text: str) -> (float, float):
        max_score = 0
        total_score = 0
        unique_list = self.analyze(text)
        for pii in unique_list:
            score = pii.score
            if score > max_score:
                max_score = score
            total_score += score
        return max_score, total_score

    def pseudo(self, text: str) -> (str, dict):
        pii_list = self.analyze(text)
        replacement_map = {}
        reverse_map = {}
        for pii in pii_list:
            old_val = text[int(pii.start): int(pii.end)]
            if old_val in reverse_map:
                new_val = reverse_map[old_val]
            else:
                new_val = self.dummy_data.gen_fake_data( pii.entity_type)
                replacement_map[new_val] = old_val
            text = text[:pii.start] + new_val + text[pii.end:]
            reverse_map[old_val] = new_val
        return text, replacement_map

    def revert(self, text: str, replacement_map: dict) -> str:
        for key, value in replacement_map.items():
            text = text.replace(key, value)
        return text
