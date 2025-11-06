from __future__ import annotations

from dataclasses import dataclass
from typing import List


def _aplit_env_list(value: int) -> List[str]:
    return [item.strip() for item in value.split(',') if item.strip()]


@dataclass(frozen=True)
class PromptShieldConfig:
    high_risk_terms: List[str]
    medium_risk_terms: List[str]
    max_prompt_length: int
