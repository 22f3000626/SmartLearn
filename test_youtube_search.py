#!/usr/bin/env python3
"""
Test script for YouTube search functionality
"""

import logging
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_youtube_search():
    """Test the YouTube search functionality"""
    try:
        from services.youtubescrapper import search_youtube
        
        print("=" * 50)
        print("Testing YouTube Search Functionality")
        print("=" * 50)
        
        # Test topics
        test_topics = [
            "Python Programming",
            "Machine Learning",
            "Web Development"
        ]
        
        for topic in test_topics:
            print(f"\n🔍 Testing search for: {topic}")
            print("-" * 30)
            
            try:
                videos = search_youtube(topic)
                
                if videos:
                    print(f"✅ Found {len(videos)} videos for '{topic}'")
                    for i, video in enumerate(videos, 1):
                        print(f"  {i}. {video['title'][:60]}...")
                        print(f"     Duration: {video['duration_mins']} min")
                        print(f"     Views: {video['views']:,}")
                        print(f"     URL: {video['url']}")
                        print()
                else:
                    print(f"❌ No videos found for '{topic}'")
                    
            except Exception as e:
                print(f"❌ Error searching for '{topic}': {e}")
                
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the project directory")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_youtube_search() 