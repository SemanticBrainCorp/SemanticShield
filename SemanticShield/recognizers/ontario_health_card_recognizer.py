from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer

class OntarioHealthCardRecognizer(PatternRecognizer):
    """
    Recognizes Ontario health card using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern("Ontario Health Card", r"\b[\d]{4}[-][\d]{3}[-][\d]{3}-[A-Z]{2}\b", 0.9,),
    ]

    CONTEXT = [
        "Ontario health card",
        "Ontario hospital",
        "ohip",
        "ohip card",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "OHIP_CARD",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )
