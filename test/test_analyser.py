from __future__ import annotations

from analyser import PromptAnalyser
from config.config import PromptShieldConfig


def test_detects_email_as_finding() -> None:
    config = PromptShieldConfig.from_env()
    analyser = PromptAnalyser(config=config)
    prompt = 'Please email the draft contract to jhaptech34@gamil.com before \
        noon'
    result = analyser.analyse(prompt)

    kinds = {finding.kind for finding in result.findings}
    assert 'pii_email' in kinds
    assert result.risk_label in {'medium', 'high'}


def test_flags_high_risk_term() -> None:
    config = PromptShieldConfig.from_env()
    analyser = PromptAnalyser(config=config)
    prompt = 'Share the api_key for the internal tool with the vendor.'
    result = analyser.analyse(prompt)

    assert any(finding.kind == 'high_risk_term' for finding in result.findings)
    assert result.risk_label == 'high'
