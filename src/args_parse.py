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

VALID_MODELS = [
    "gemini-2.0-flash-lite-preview-02-05",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]

def get_summarize_args() -> Tuple[str, str, str]:
    """Get and parse command line arguments for summarize command
    
    Returns:
        Tuple of (youtube_url, format, model)
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
    model: str = typer.Option(
        VALID_MODELS[0],
        "--model",
        "-m",
        help="Gemini model to use for analysis",
    )
    return youtube_url, format, model
