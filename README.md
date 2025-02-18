# YouTube Transcript Summarizer

A command-line tool to fetch and summarize YouTube video transcripts using Google's Gemini AI.

## Installation

```bash
pip install .
```

## Usage

The URL must be enclosed in quotes to prevent shell interpretation of special characters:

```bash
uv run summarize "https://www.youtube.com/watch?v=VIDEO_ID"
```

Options:
- `--model`: Model name (default: gemini-2.0-flash)
- `--format`: Output format (default: md)
- `--lang`: Transcript language (default: en)

Example:
```bash
uv run summarize "https://www.youtube.com/watch?v=bAAbrhb3QoM" --format txt
```
