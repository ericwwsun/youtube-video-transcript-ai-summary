# YouTube Transcript Summarizer

A command-line tool to fetch and summarize YouTube video transcripts using Google's Gemini AI.

## Installation

```bash
pip install .
```

## Setup

1. Create a `.env` file in the project root
2. Add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

The URL must be enclosed in quotes to prevent shell interpretation of special characters:

```bash
uv run summarize "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Options
- `--model`: Gemini model name (default: gemini-2.0-flash)
- `--format`: Output format, either 'json' or 'md' (default: md)

### Example
```bash
uv run summarize "https://www.youtube.com/watch?v=bAAbrhb3QoM" --format json
```

### Output
Summaries are saved in the `transcript_output` directory with the video ID as the filename and the appropriate extension (`.md` or `.json`).
