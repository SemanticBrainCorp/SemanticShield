from dataclasses import dataclass, field
from typing import Optional, Type

@dataclass
class ShieldResult:
    fail: bool
    message: str
    pii_max: Optional[float]=0
    pii_total: Optional[float]=0
    sanitized: Optional[str]=None
    replacement_map: Optional[dict]=None
    usage: Optional[float]=0