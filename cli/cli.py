from __future__ import annotations

import json
import logging
from argparse import ArgumentParser
from pathlib import Path
from sys import exit, stdin
from typing import Optional

from Prompt_Shield.analyser import PromptAnalyser
from Prompt_Shield.config.config import PromptShieldConfig


def _read_input_text(file_path: Optional[Path], text: Optional[str]) -> str:
    """
    Resolve the prompt text from CLI arguments or stdin.

    Preference order: explicit --text value, file content, then piped stdin.
    """

    if text:
        return text

    if file_path:
        if not file_path.exists():
            raise FileNotFoundError(f'File not found: {file_path}')

        return file_path.read_text(encoding='utf-8')

    stdin_data: str = stdin.read()
    if stdin_data.strip():
        return stdin_data

    raise ValueError(
        'No input provided. Use --text, --file or pipe data via stdin.'
    )


def _build_parser() -> ArgumentParser:
    """Construct and return the CLI argument parser."""

    parser = ArgumentParser(
        prog='Prompt_Shield',
        description=(
            'Prompt_Shield scans prompts for risky content before sending to \
                LLMs.'
        ),
    )

    parser.add_argument(
        '--text',
        type=str,
        help='The prompt text to analyse.',
    )
    parser.add_argument(
        '--file',
        type=Path,
        help='Path to a file containing the prompt.',
    )
    parser.add_argument(
        '--format',
        choices=('text', 'json'),
        default='text',
        help='Choose plain text or JSON output.',
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable debug logging.',
    )

    return parser


def run_cli() -> None:
    """Entrypoint used by the Prompt_Shield console script."""

    parser = _build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    )
    logger: logging.Logger = logging.getLogger('cli.cli')

    try:
        prompt_text: str = _read_input_text(args.file, args.text)

    except (FileNotFoundError, ValueError) as prompt_err:
        logger.error('%s', prompt_err)
        exit(1)

    config: PromptShieldConfig = PromptShieldConfig.from_env()
    analyser: PromptAnalyser = PromptAnalyser(
        config=config, logger=logging.getLogger('analyser')
    )

    result = analyser.analyse(prompt_text)

    if args.format == 'json':
        print(json.dumps(result.to_dict(), indent=2))
        return

    print(
        f'Prompt_Shield Risk: {result.risk_label.upper()} \
            {result.total_risk_score}'
    )
    print(f'Prompt length: {result.prompt_length} characters')

    if not result.findings:
        print('✅ No risky content detected. Prompt looks clean.')
        return

    print('\nFindings:')
    for idx, finding in enumerate(result.findings, start=1):
        print(f' {idx}. [{finding.severity.upper()}] {finding.kind}')
        print(f'    → {finding.description}')
        print(f'    → Snippet: {finding.snippet}')
        print(f'    → Span: {finding.span}')
