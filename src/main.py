import re
import os
import typer
import logging
from pathlib import Path
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
from src.data_type import TranscriptAnalysis
from src.output_format import format_as_markdown, format_as_json
from src import args_parse

# Load environment variables
load_dotenv()

# Configure Google Generative AI
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it in your .env file.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer()

def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL
    
    Args:
        url: YouTube URL (e.g., https://www.youtube.com/watch?v=LkDelp5WWYU)
        
    Returns:
        The video ID string
        
    Raises:
        ValueError: If the URL format is invalid
    """
    pattern = r"(?:youtube\.com\/watch\?v=|youtu\.be\/)([A-Za-z0-9_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def summarize(
    youtube_url: str = args_parse.get_summarize_args()[0],
    format: str = args_parse.get_summarize_args()[1],
    model: str = args_parse.get_summarize_args()[2]
):
    """Process a YouTube video URL"""
    try:
        video_id = extract_video_id(youtube_url)
        logger.info(f"Successfully extracted video ID: {video_id}")
        
        # Fetch transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript_text = " ".join([item['text'] for item in transcript_list])

        # Generate summary using Gemini
        client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})

        response = client.models.generate_content(
            model=f'models/{model}',
            contents=[f"Please provide a concise summary of the transcript. Use this URL for the video_url field: {youtube_url}\n\n{transcript_text}"],
            config={
                'response_mime_type': 'application/json',
                'response_schema': TranscriptAnalysis,
            },
        )
        
        # Get the parsed analysis
        analysis = response.parsed
        
        # Format the analysis based on format option
        if format.lower() == "json":
            output = format_as_json(analysis)
            extension = ".json"
        else:  # default to markdown
            output = format_as_markdown(analysis)
            extension = ".md"
        
        # Create filename using video ID and format extension
        filename = f"{video_id}{extension}"
        
        # Ensure transcript directory exists
        transcript_dir = Path("transcript")
        transcript_dir.mkdir(exist_ok=True)
        
        # Save the file
        output_path = transcript_dir / filename
        output_path.write_text(output)
        
        logger.info(f"Analysis saved to: {output_path}")
        print(output)
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
else:
    # This allows the function to be called directly via `uv run summarize`
    typer.run(summarize)
