import json
from src.data_type import TranscriptAnalysis

def format_as_json(analysis: TranscriptAnalysis) -> str:
    """Format the TranscriptAnalysis object as JSON
    
    Args:
        analysis: A TranscriptAnalysis object containing the analysis results
        
    Returns:
        A formatted JSON string
    """
    return json.dumps(analysis.model_dump(), indent=2)

def format_as_markdown(analysis: TranscriptAnalysis) -> str:
    """Format the TranscriptAnalysis object as markdown
    
    Args:
        analysis: A TranscriptAnalysis object containing the analysis results
        
    Returns:
        A formatted markdown string
    """
    output = []
    output.append(f"# {analysis.video_title}\n")
    output.append("#transcript")
    output.append(f"\n[Watch Video]({analysis.video_url})")
    output.append(f"\n**Published Date: {analysis.video_publish_date}**")
    output.append(f"\n**Summarized By: {analysis.summarize_by_model}**")
    output.append(f"\n**Date Created: {analysis.create_date}**")
    output.append(f"\n## Quick Summary\n{analysis.quick_summary}")
    output.append("\n## Bullet Point Highlights")
    for highlight in analysis.bullet_point_highlights:
        output.append(f"* {highlight}")
    
    output.append("\n## Sections")
    for section in analysis.sections:
        output.append(f"\n### {section.section_title}")
        output.append(f"\n{section.section_summary}")
        
    output.append(f"\n## Sentiment Analysis\n{analysis.sentiment_analysis}")
    output.append("\n## Keywords")
    for keyword in analysis.keywords:
        output.append(f"* {keyword}")
    
    return "\n".join(output)
