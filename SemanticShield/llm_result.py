from dataclasses import dataclass

@dataclass
class LLMCheckResult:
    fail: bool
    usage: float
