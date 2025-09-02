"""
Command-line interface for testing the LinkedIn post text extractor.
"""

import asyncio
import json
import sys
from typing import Optional

import click

from linkedin_extractor import LinkedInExtractor


async def async_extract_post_text(url: str, output, pretty: bool, verbose: bool):
    """Async wrapper for the extraction logic."""
    if verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    extractor = LinkedInExtractor()
    
    try:
        click.echo(f"Extracting text from: {url}", err=True)
        result = await extractor.extract_post_text(url)
        
        if pretty:
            json_output = json.dumps(result, indent=2, ensure_ascii=True)
        else:
            json_output = json.dumps(result, ensure_ascii=True)
        
        # Handle encoding for Windows console
        try:
            click.echo(json_output, file=output)
        except UnicodeEncodeError:
            # Fallback: encode as UTF-8 and print safely
            safe_output = json_output.encode('utf-8', errors='replace').decode('utf-8')
            click.echo(safe_output, file=output)
        
        if not result.get('success'):
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@click.command()
@click.argument('url')
@click.option('--output', '-o', type=click.File('w'), default=sys.stdout,
              help='Output file (default: stdout)')
@click.option('--pretty', '-p', is_flag=True, default=True,
              help='Pretty print JSON output')
@click.option('--verbose', '-v', is_flag=True,
              help='Enable verbose logging')
def main(url: str, output, pretty: bool, verbose: bool):
    """Extract text from a LinkedIn post URL."""
    asyncio.run(async_extract_post_text(url, output, pretty, verbose))


if __name__ == "__main__":
    main()