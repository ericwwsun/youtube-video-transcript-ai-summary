import typer
import re
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai

app = typer.Typer()

def extract_video_id(url: str) -> str:
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

@app.command()
def summarize(
    url: str = typer.Argument(..., help="YouTube URL (must be in quotes)"),
    model: str = typer.Option("gemini-2.0-flash", help="Model name"),
    format: str = typer.Option("md", help="Output format"),
    lang: str = typer.Option("en", help="Transcript language")
):
    """
    Fetch and summarize a YouTube video transcript.
    The URL must be enclosed in quotes, e.g.: "https://www.youtube.com/watch?v=VIDEO_ID"
    """
    try:
        # Extract the video ID from the URL
        video_id = extract_video_id(url)

        # Fetch the transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        transcript_text = " ".join([item['text'] for item in transcript_list])

        # Initialize the Google GenAI client
        client = genai.Client()

        # Create the prompt for summarization
        prompt = f"Summarize the following transcript in {format} format:\n{transcript_text}"

        # Generate the summary using the specified model
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        # Store the summarized output in the filesystem
        output_file = f"summary.{format}"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response.text)

        # Inform the user that the summary has been saved
        print(f"Summary saved to {output_file}")
        
    except Exception as e:
        typer.echo(f"An error occurred: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
