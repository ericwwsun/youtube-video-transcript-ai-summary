import typer
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer()

def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL"""
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

@app.command()
def summarize(
    youtube_url: str = typer.Argument(..., help="YouTube URL (must be in quotes)")
):
    """Process a YouTube video URL"""
    try:
        video_id = extract_video_id(youtube_url)
        logger.info(f"Successfully extracted video ID: {video_id}")
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
