from __future__ import annotations

from dataclasses import dataclass
from os import environ
from typing import List


def _split_env_list(value: str) -> List[str]:
    """
    Split a comma-separated environment variable into a list of clean terms.
    """
    return [item.strip() for item in value.split(',') if item.strip()]


@dataclass(frozen=True)
class PromptShieldConfig:
    """Immutable configuration container for the analyser."""

    high_risk_terms: List[str]
    medium_risk_terms: List[str]
    max_prompt_length: int

    @classmethod
    def from_env(psc_class) -> 'PromptShieldConfig':
        """
        Build a configuration instance from environment variables.

        Defaults are applied when specific variables are not provided.
        """

        high_risk_raw = environ.get(
            'PROMPT_SHIELD_HIGH_RISK_TERMS',
            'api_key,ssh_key,trade_secret,customer_ssn',
        )
        medium_risk_raw = environ.get(
            'PROMPT_SHIELD_MEDIUM_RISK_TERMS',
            'password,internal_only,confidential',
        )
        max_length_raw = environ.get('PROMPT_SHIELD_MAX_PROMPT_LENGTH', '1500')

        try:
            max_prompt_length = int(max_length_raw)

        except ValueError as ve:
            raise ValueError(
                'PROMPT_SHIELD_MAX_PROMPT_LENGTH must be an integer!'
            ) from ve

        return psc_class(
            high_risk_terms=_split_env_list(high_risk_raw),
            medium_risk_terms=_split_env_list(medium_risk_raw),
            max_prompt_length=max_prompt_length,
        )
