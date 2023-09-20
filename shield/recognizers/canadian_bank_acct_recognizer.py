from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class CanadianBankAccountRecognizer(PatternRecognizer):
    """
    Recognizes Canadian Bank Account Number using regex.
    
    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern("CA_BANK_ACCT", r"\b(\d{5}-\d{3}-\d{7})|(\d{9})\b", 0.9),
    ]
    CONTEXT = [
        "ca",
        "canada", 
        "check",
        "account",
        "account#",
        "acct",
        "save",
        "debit",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "CA_BANK_ACCT",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )
