from pydantic import BaseModel
from typing import List

class TranscriptAnalysis(BaseModel):
    """Model for storing transcript analysis results"""
    quick_summary: str
    bullet_point_highlights: List[str]
    sentiment_analysis: str
    keywords: List[str]
