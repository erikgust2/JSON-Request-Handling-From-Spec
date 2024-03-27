from dataclasses import dataclass, field, asdict
from typing import List, Optional
import json

@dataclass
class request:
    A: int = None
    B: str = None
    C: float = None
    D: List[bool] = field(default_factory=list)

    @classmethod
    def from_json(cls, json_str: str):
        return cls(**json.loads(json_str))

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str)
