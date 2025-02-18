import typer
from typing import Tuple

def parse_youtube_url(url: str) -> str:
    """Callback to clean YouTube URL
    
    Args:
        url: Raw YouTube URL input
        
    Returns:
        Cleaned URL string with quotes stripped
    """
    return url.strip("\"'")

def get_summarize_args() -> Tuple[str, str]:
    """Get and parse command line arguments for summarize command
    
    Returns:
        Tuple of (youtube_url, format)
    """
    youtube_url: str = typer.Argument(
        ...,
        help="YouTube URL",
        callback=parse_youtube_url
    )
    format: str = typer.Option(
        "md",
        "--format",
        "-f",
        help="Output format: 'md' or 'json'"
    )
    return youtube_url, format
