from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Literal

risk_level = Literal['low', 'medium', 'high']


@dataclass(frozen=True)
class Finding:
    kind: str
    severity: risk_level
    description: str
    snippet: str
    span: tuple[int, int]


@dataclass(frozen=True)
class AnalysisResult:
    prompt_length: int
    findings: List[Finding] = field(default_factory=list)
    total_risk_score: int = 0
    risk_label: risk_level = 'low'
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            'prompt_length': self.prompt_length,
            'findings': [
                {
                    'kind': finding.kind,
                    'severity': finding.severity,
                    'description': finding.description,
                    'snippet': finding.snippet,
                    'span': finding.span,
                } for finding in self.findings
            ],
            'total_risk_score': self.total_risk_score,
            'risk_label': self.risk_label,
            'metadata': self.metadata,
        }
