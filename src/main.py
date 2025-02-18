import typer
import re
import os
import logging
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
from src.data_type import TranscriptAnalysis
from src.output_format import format_as_markdown

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
        
        # Fetch transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript_text = " ".join([item['text'] for item in transcript_list])

        # Generate summary using Gemini
        # prompt = f"Please provide a concise summary of this video transcript:\n\n{transcript_text}"
        # response = model.generate_content(prompt)

        client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})

        response = client.models.generate_content(
            model='models/gemini-1.5-flash',
            contents=[f"Please provide a concise summary of the transcript:\n\n{transcript_text}"],
            config={
                'response_mime_type': 'application/json',
                'response_schema': TranscriptAnalysis,
            },
        )

        # Format and log the analysis
        markdown_output = format_as_markdown(response.text)
        logger.info("Generated Analysis (Markdown format):")
        print(markdown_output)
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
