"""MCP Server for the dair-ai/emotion dataset."""

import json
import random
from typing import Optional, List, Dict, Any
from enum import Enum

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
from datasets import load_dataset


# Initialize MCP server
mcp = FastMCP("emotion_mcp")

# Load dataset at module level for reuse
DATASET = None


def _load_dataset() -> Any:
    """Load the emotion dataset lazily."""
    global DATASET
    if DATASET is None:
        DATASET = load_dataset("dair-ai/emotion", split="train")
    return DATASET


class EmotionType(str, Enum):
    """Available emotion labels in the dataset."""
    SADNESS = "sadness"
    JOY = "joy"
    LOVE = "love"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"


# Mapping of emotion label indices to names
EMOTION_LABELS = {
    0: "sadness",
    1: "joy", 
    2: "love",
    3: "anger",
    4: "fear",
    5: "surprise"
}


# ============================================================================
# Tool 1: Get Random Samples
# ============================================================================

class GetSampleInput(BaseModel):
    """Input model for get_sample tool."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    n: int = Field(
        default=3,
        description="Number of random samples to retrieve",
        ge=1,
        le=100
    )


@mcp.tool(
    name="get_sample",
    annotations={
        "title": "Get Random Samples",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,  # Random results
        "openWorldHint": False
    }
)
async def get_sample(params: GetSampleInput) -> str:
    """Get n random samples from the emotion dataset.
    
    This tool retrieves random text samples with their emotion labels.
    Useful for exploring the dataset or getting examples.
    
    Args:
        params (GetSampleInput): Contains:
            - n (int): Number of samples (1-100)
    
    Returns:
        str: JSON array of samples, each containing:
            - text (str): The text content
            - emotion (str): The emotion label
            - label_id (int): Numeric label (0-5)
    """
    try:
        dataset = _load_dataset()
        
        # Get random indices
        total_size = len(dataset)
        indices = random.sample(range(total_size), min(params.n, total_size))
        
        # Get samples
        samples = []
        for idx in indices:
            item = dataset[idx]
            samples.append({
                "text": item["text"],
                "emotion": EMOTION_LABELS[item["label"]],
                "label_id": item["label"]
            })
        
        return json.dumps(samples, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to get samples: {str(e)}"
        }, indent=2)


# ============================================================================
# Tool 2: Count by Emotion
# ============================================================================

class CountByEmotionInput(BaseModel):
    """Input model for count_by_emotion tool."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    emotion: EmotionType = Field(
        description="Emotion to count (sadness, joy, love, anger, fear, surprise)"
    )


@mcp.tool(
    name="count_by_emotion",
    annotations={
        "title": "Count Samples by Emotion",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def count_by_emotion(params: CountByEmotionInput) -> str:
    """Count the number of samples for a specific emotion.
    
    This tool returns the count of text samples labeled with the specified emotion.
    
    Args:
        params (CountByEmotionInput): Contains:
            - emotion (str): One of: sadness, joy, love, anger, fear, surprise
    
    Returns:
        str: JSON object containing:
            - emotion (str): The queried emotion
            - count (int): Number of samples with this emotion
            - total (int): Total dataset size
            - percentage (float): Percentage of dataset
    """
    try:
        dataset = _load_dataset()
        
        # Find the label ID for this emotion
        label_id = None
        for lid, label_name in EMOTION_LABELS.items():
            if label_name == params.emotion:
                label_id = lid
                break
        
        if label_id is None:
            return json.dumps({
                "error": f"Unknown emotion: {params.emotion}"
            }, indent=2)
        
        # Count samples with this label
        count = sum(1 for item in dataset if item["label"] == label_id)
        total = len(dataset)
        
        result = {
            "emotion": params.emotion,
            "count": count,
            "total": total,
            "percentage": round((count / total * 100), 2) if total > 0 else 0
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to count by emotion: {str(e)}"
        }, indent=2)


# ============================================================================
# Tool 3: Search Text
# ============================================================================

class SearchTextInput(BaseModel):
    """Input model for search_text tool."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    query: str = Field(
        description="Text to search for in samples",
        min_length=1,
        max_length=200
    )
    
    limit: int = Field(
        default=10,
        description="Maximum number of results to return",
        ge=1,
        le=100
    )


@mcp.tool(
    name="search_text",
    annotations={
        "title": "Search Text in Samples",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def search_text(params: SearchTextInput) -> str:
    """Search for text within the dataset samples.
    
    This tool performs a case-insensitive substring search across all text samples
    and returns matching results with their emotion labels.
    
    Args:
        params (SearchTextInput): Contains:
            - query (str): Search query text
            - limit (int): Max results (1-100, default 10)
    
    Returns:
        str: JSON object containing:
            - query (str): The search query
            - count (int): Number of results found
            - results (list): Matching samples with text and emotion
    """
    try:
        dataset = _load_dataset()
        query_lower = params.query.lower()
        
        # Search through dataset
        results = []
        for item in dataset:
            if query_lower in item["text"].lower():
                results.append({
                    "text": item["text"],
                    "emotion": EMOTION_LABELS[item["label"]],
                    "label_id": item["label"]
                })
                
                if len(results) >= params.limit:
                    break
        
        response = {
            "query": params.query,
            "count": len(results),
            "results": results
        }
        
        return json.dumps(response, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to search text: {str(e)}"
        }, indent=2)


# ============================================================================
# Tool 4: Analyze Emotion Distribution
# ============================================================================

@mcp.tool(
    name="analyze_emotion_distribution",
    annotations={
        "title": "Analyze Emotion Distribution",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def analyze_emotion_distribution() -> str:
    """Get statistical distribution of emotions across the dataset.
    
    This tool analyzes the entire dataset and provides counts and percentages
    for each emotion label.
    
    Returns:
        str: JSON object containing:
            - total_samples (int): Total number of samples
            - distribution (list): For each emotion:
                - emotion (str): Emotion name
                - count (int): Number of samples
                - percentage (float): Percentage of dataset
    """
    try:
        dataset = _load_dataset()
        
        # Count each emotion
        emotion_counts = {label: 0 for label in EMOTION_LABELS.values()}
        
        for item in dataset:
            emotion_name = EMOTION_LABELS[item["label"]]
            emotion_counts[emotion_name] += 1
        
        total = len(dataset)
        
        # Build distribution
        distribution = []
        for emotion, count in sorted(emotion_counts.items()):
            distribution.append({
                "emotion": emotion,
                "count": count,
                "percentage": round((count / total * 100), 2) if total > 0 else 0
            })
        
        result = {
            "total_samples": total,
            "distribution": distribution
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to analyze distribution: {str(e)}"
        }, indent=2)


# ============================================================================
# Server Entry Point
# ============================================================================

if __name__ == "__main__":
    mcp.run()
