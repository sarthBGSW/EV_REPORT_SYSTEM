from typing import List, TypedDict

__all__ = ['AgentState']

class AgentState(TypedDict):
    topic: str
    uploaded_context: str
    outline: List[str]  # List of Chapter Titles
    current_chapter_index: int
    current_chapter_content: str
    research_notes: str
    reviews: str
    final_document: str