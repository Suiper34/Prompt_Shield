# utils.py
"""Data models for Prompt Shield analysis outputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Tuple

RiskLevel = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class Finding:
    """Represents a single risky observation discovered during analysis."""

    kind: str
    severity: RiskLevel
    description: str
    snippet: str
    span: Tuple[int, int]


@dataclass(frozen=True)
class AnalysisResult:
    """Aggregates the outcome of analysing a prompt for risky content."""

    prompt_length: int
    findings: List[Finding] = field(default_factory=list)
    total_risk_score: int = 0
    risk_label: RiskLevel = 'low'
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the analysis result to a JSON-friendly dictionary."""

        return {
            'prompt_length': self.prompt_length,
            'findings': [
                {
                    'kind': finding.kind,
                    'severity': finding.severity,
                    'description': finding.description,
                    'snippet': finding.snippet,
                    'span': finding.span,
                }
                for finding in self.findings
            ],
            'total_risk_score': self.total_risk_score,
            'risk_label': self.risk_label,
            'metadata': self.metadata,
        }
