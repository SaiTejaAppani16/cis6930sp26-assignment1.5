#!/usr/bin/env python3
"""Test script for Emotion MCP Server."""

import asyncio
import sys
from server import (
    get_sample, 
    count_by_emotion, 
    search_text, 
    analyze_emotion_distribution,
    GetSampleInput,
    CountByEmotionInput, 
    SearchTextInput
)


async def test_all_tools():
    """Test all MCP tools."""
    
    print("=" * 70)
    print("Testing Emotion MCP Server")
    print("=" * 70)
    
    # Test 1: get_sample
    print("\n" + "=" * 70)
    print("get_sample(n=3)")
    print("=" * 70)
    try:
        result = await get_sample(GetSampleInput(n=3))
        print(result)
        print("✓ Passed")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    # Test 2: count_by_emotion
    print("\n" + "=" * 70)
    print("count_by_emotion(emotion='joy')")
    print("=" * 70)
    try:
        result = await count_by_emotion(CountByEmotionInput(emotion="joy"))
        print(result)
        print("✓ Passed")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    # Test 3: search_text
    print("\n" + "=" * 70)
    print("search_text(query='happy', limit=10)")
    print("=" * 70)
    try:
        result = await search_text(SearchTextInput(query="happy", limit=10))
        print(result)
        print("✓ Passed")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    # Test 4: analyze_emotion_distribution
    print("\n" + "=" * 70)
    print("analyze_emotion_distribution()")
    print("=" * 70)
    try:
        result = await analyze_emotion_distribution()
        print(result)
        print("✓ Passed")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("All tests passed!")
    print("=" * 70)
    
    return True


async def test_individual_emotions():
    """Test all emotion types."""
    print("\n" + "=" * 70)
    print("Testing all emotions")
    print("=" * 70)
    
    emotions = ["sadness", "joy", "love", "anger", "fear", "surprise"]
    
    for emotion in emotions:
        try:
            result = await count_by_emotion(CountByEmotionInput(emotion=emotion))
            print(f"\n{emotion.upper()}:")
            print(result)
        except Exception as e:
            print(f"Error testing {emotion}: {e}")


if __name__ == "__main__":
    try:
        success = asyncio.run(test_all_tools())
        
        if success and "--all" in sys.argv:
            asyncio.run(test_individual_emotions())
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
