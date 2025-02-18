from src.data_type import TranscriptAnalysis

def format_as_markdown(analysis: TranscriptAnalysis) -> str:
    """Format the analysis results as markdown"""
    markdown = f"""# Video Transcript Analysis

## Summary
{analysis.quick_summary}

## Key Highlights
{"".join([f'- {point}\n' for point in analysis.bullet_point_highlights])}
## Sentiment Analysis
{analysis.sentiment_analysis}

## Keywords
{', '.join(analysis.keywords)}
"""
    return markdown
