from src.data_type import TranscriptAnalysis

def format_as_markdown(analysis: TranscriptAnalysis) -> str:

    print(analysis.quick_summary)

    """Format the analysis results as markdown"""
    output = []
    output.append("# Transcript Analysis")
    output.append(f"\n## Quick Summary\n{analysis.quick_summary}")
    output.append("\n## Bullet Point Highlights")
    for highlight in analysis.bullet_point_highlights:
        output.append(f"* {highlight}")
    output.append(f"\n## Sentiment Analysis\n{analysis.sentiment_analysis}")
    output.append("\n## Keywords")
    for keyword in analysis.keywords:
        output.append(f"* {keyword}")
    return "\n".join(output)
