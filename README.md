# Emotion MCP Server

An MCP (Model Context Protocol) server for analyzing and processing the dair-ai/emotion dataset. This dataset contains 16,000 text samples labeled with six different emotions: sadness, joy, love, anger, fear, and surprise.

## Description

This server provides a programmatic interface to explore and analyze emotional text data through four specialized tools. It's designed to help understand the distribution of emotions in text and search for specific patterns across the dataset.

## Tools

### 1. get_sample(n)
Get random samples from the dataset.

**Input:**
- `n` (int): Number of samples to retrieve (1-100)

**Output:**
```json
[
  {
    "text": "i feel tortured the one thing i love is...",
    "emotion": "anger",
    "label_id": 3
  }
]
```

### 2. count_by_emotion(emotion)
Count samples for a specific emotion.

**Input:**
- `emotion` (str): One of: sadness, joy, love, anger, fear, surprise

**Output:**
```json
{
  "emotion": "joy",
  "count": 5362,
  "total": 16000,
  "percentage": 33.51
}
```

### 3. search_text(query, limit)
Search for text in samples.

**Input:**
- `query` (str): Search text
- `limit` (int, optional): Max results (default: 10)

**Output:**
```json
{
  "query": "happy",
  "count": 10,
  "results": [
    {
      "text": "i feel very happy and excited...",
      "emotion": "joy",
      "label_id": 1
    }
  ]
}
```

### 4. analyze_emotion_distribution()
Get statistics about emotion distribution across the entire dataset.

**Input:** None

**Output:**
```json
{
  "total_samples": 16000,
  "distribution": [
    {
      "emotion": "anger",
      "count": 2159,
      "percentage": 13.49
    },
    {
      "emotion": "joy",
      "count": 5362,
      "percentage": 33.51
    }
  ]
}
```

## Setup

### Local Testing

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install mcp datasets pydantic
python test_tools.py
```

### HiPerGator

```bash
# Request compute node
srun --partition=hpg-default --ntasks=1 --cpus-per-task=2 --mem=4gb --time=02:00:00 --pty bash

# Run setup
chmod +x setup.sh
./setup.sh
```

## Running

```bash
# Test all tools
python test_tools.py

# Run the MCP server
python server.py
```

## Dataset Information

**Source:** dair-ai/emotion (Hugging Face)
**Size:** 16,000 samples
**Emotions:** 
- sadness (0) - 29.16%
- joy (1) - 33.51%
- love (2) - 8.15%
- anger (3) - 13.49%
- fear (4) - 12.11%
- surprise (5) - 3.57%