import typer
import re
import os
import logging
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Configure Google Generative AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

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
        prompt = f"Please provide a concise summary of this video transcript:\n\n{transcript_text}"
        response = model.generate_content(prompt)
        
        # Log the summary
        logger.info("Generated Summary:")
        logger.info(response.text)
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
