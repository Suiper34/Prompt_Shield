from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple

from Prompt_Shield.config.config import PromptShieldConfig
from Prompt_Shield.detectors import find_pii_matches, find_term_matches
from Prompt_Shield.utils import AnalysisResult, Finding, RiskLevel


def _window_snippet(
    prompt: str,
    span: Tuple[int, int],
    radius: int = 25,
) -> str:
    """
    Extract a contextual snippet around a span of text.

    The snippet spans `radius` characters to the left and right of the match.
    """

    start = max(span[0] - radius, 0)
    end = min(span[1] + radius, len(prompt))
    snippet = prompt[start:end].replace('\n', ' ').strip()

    return snippet


class PromptAnalyser:
    """
    Detects risky content inside prompts before dispatching to LLMs.
    """

    _PII_SEVERITY: Dict[str, RiskLevel] = {
        'email': 'medium',
        'phone_number': 'medium',
        'ipv4': 'medium',
        'credit_card': 'high',
        'ssn': 'high',
    }

    def __init__(
        self,
        config: PromptShieldConfig,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        Initialise the analyser with configuration and an optional logger.
        """

        self.config = config
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    def analyse(self, prompt: str) -> AnalysisResult:
        """
        Analyse the provided prompt and return structured findings.
        """

        prompt_length: int = len(prompt)
        findings: List[Finding] = []

        # PII detection
        for kind, match_value, span in find_pii_matches(prompt):
            severity: RiskLevel = self._PII_SEVERITY.get(kind, 'medium')
            description = f'Detected potential {kind.replace("_", " ")}.'
            findings.append(
                Finding(
                    kind=f'pii_{kind}',
                    severity=severity,
                    description=description,
                    snippet=_window_snippet(prompt, span),
                    span=span,
                )
            )
            self.logger.debug('PII finding registered: %s at span %s.',
                              kind,
                              span)

        # high-risk terminology
        for term, span in find_term_matches(prompt,
                                            self.config.high_risk_terms):
            description = f'High risk term "{term}" was found.'
            findings.append(
                Finding(
                    kind='high_risk_term',
                    severity='high',
                    description=description,
                    snippet=_window_snippet(prompt, span),
                    span=span,
                )
            )
            self.logger.debug('High risk term detected: %s at span %s.',
                              term,
                              span)

        # medium-risk terminology
        for term, span in find_term_matches(prompt,
                                            self.config.medium_risk_terms):
            description = f'Medium risk term "{term}" was found.'
            findings.append(
                Finding(
                    kind='medium_risk_term',
                    severity='medium',
                    description=description,
                    snippet=_window_snippet(prompt, span),
                    span=span,
                )
            )
            self.logger.debug('Medium risk term detected: %s at span %s.',
                              term,
                              span)

        # length enforcement
        if prompt_length > self.config.max_prompt_length:
            overage = prompt_length - self.config.max_prompt_length
            severity = (
                'high'
                if prompt_length > int(self.config.max_prompt_length * 1.2)
                else 'medium'
            )
            description = (
                f'Prompt length exceeded by {overage} characters '
                f'(max {self.config.max_prompt_length}).'
            )
            snippet_span = (
                self.config.max_prompt_length,
                min(prompt_length, self.config.max_prompt_length + 40),
            )
            findings.append(
                Finding(
                    kind='length_violation',
                    severity=severity,
                    description=description,
                    snippet=_window_snippet(prompt, snippet_span),
                    span=snippet_span,
                )
            )
            self.logger.debug(
                'Length violation detected: %d characters over limit.', overage
            )

        score_map: Dict[RiskLevel, int] = {'low': 1, 'medium': 2, 'high': 3}
        total_risk_score: int = sum(
            score_map[finding.severity] for finding in findings
        )

        if any(
                    finding.severity == 'high' for finding in findings
                ) or total_risk_score >= 15:
            risk_label: RiskLevel = 'high'

        elif total_risk_score >= 6:
            risk_label = 'medium'

        else:
            risk_label = 'low'

        self.logger.debug(
            'Analysis complete! Total findings: %d, risk score: %d, label: %s',
            len(findings),
            total_risk_score,
            risk_label,
        )

        metadata = {
            'max_prompt_length': self.config.max_prompt_length,
            'finding_count': len(findings),
            'config': {
                'high_risk_terms': self.config.high_risk_terms,
                'medium_risk_terms': self.config.medium_risk_terms,
            },
        }

        return AnalysisResult(
            prompt_length=prompt_length,
            findings=findings,
            total_risk_score=total_risk_score,
            risk_label=risk_label,
            metadata=metadata,
        )
