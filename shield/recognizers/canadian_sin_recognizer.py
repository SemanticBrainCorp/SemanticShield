from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class CanadianSINRecognizer(PatternRecognizer):
    """
    Recognizes Canadian Social Insurance Number using regex.
    TEMPORARY solution, to disambiguate from other similar patterns we should use a sin validator
    https://en.wikipedia.org/wiki/Luhn_algorithm - crypto_recognizer is a sample of regex + validation algo

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern("CA_SIN", r"\b\d{3}-\d{3}-\d{3}\b", 0.9),
    ]
    CONTEXT = ["ca", "canada", "SIN", "Social Insurance Number", "Social Insurance #"]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "CA_SIN",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )
