from dataclasses import dataclass, field
from typing import Optional, Type

@dataclass
class ShieldResult:
    fail: bool
    fail_type: Optional[str] = None
    message: Optional[str] = None
    fail_data: Optional[list] = None
    pii_max: Optional[float]=0
    pii_total: Optional[float]=0
    sanitized: Optional[str]=None
    replacement_map: Optional[dict]=None
    usage: Optional[float]=0