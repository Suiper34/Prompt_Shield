from __future__ import annotations

from re import Pattern, compile
from typing import Dict, List, Sequence, Tuple

PII_PATERNS: Dict[str, Pattern[str]] = {
    'email': compile(r'[\w\.-]+@[\w\.-]+\. \w+'),
    'phone_number': compile(
        r'\b(?:\+?d{1,3}[-.\s]?)?(?:\(\d{2,4}\)|\d{2,4})[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b'
    ),
    'ipv4': compile(
        r'\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b'
    ),
    'credit_card': compile(r'\b(?:\d[ -]?){13,16}\b'),
    'ssn': compile(r'\b\d{3}-\d{2}\d{4}\b'),
}


def findd_pii_matches(text: str) -> List[Tuple[str, str, Tuple[int, int]]]:
    matches: List[Tuple[str, str, Tuple[int, int]]] = []

    for key, pattern in PII_PATERNS.items():
        for match in pattern.finditer(text):
            matches.append((key, match.group(0), match.span()))

    return matches


def find_term_matches(
    text: str, terms: Sequence[str]
) -> List[Tuple[str, Tuple[int, int]]]:
    matches: List[Tuple[str, Tuple[int, int]]] = []
    text_lowered: str = text.lower()

    for term in terms:
        normalized_term = term.strip().lower()

        if not normalized_term:
            continue

        start = text_lowered.find(normalized_term)
        while start != -1:
            end = start + len(normalized_term)
            matches.append((term, (start, end)))

            start = text_lowered.find(normalized_term, end)

    return matches
