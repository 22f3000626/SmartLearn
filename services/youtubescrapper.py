from yt_dlp import YoutubeDL
import logging

# Initialize classifier as None, will be loaded on demand
classifier = None

def load_classifier():
    """Load the AI classifier with error handling"""
    global classifier
    if classifier is None:
        try:
            from transformers import pipeline
            classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
            logging.info("AI classifier loaded successfully")
        except Exception as e:
            logging.warning(f"Failed to load AI classifier: {e}")
            classifier = None
    return classifier

def search_youtube(topic):
    """Search YouTube for educational videos on a given topic"""
    logging.info(f"Searching YouTube for topic: {topic}")
    
    query = f"ytsearch20:{topic} tutorial -shorts"
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': False,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            logging.info(f"Executing YouTube search query: {query}")
            info = ydl.extract_info(query, download=False)
            entries = info.get('entries', [])
            logging.info(f"Found {len(entries)} raw entries from YouTube")
    except Exception as e:
        logging.error(f"YouTube search failed: {e}")
        return []

    candidates = []
    for i, entry in enumerate(entries):
        try:
            title = entry.get('title', '')
            video_id = entry.get('id', '')
            duration = entry.get('duration', 0)
            view_count = entry.get('view_count') or 0
            like_count = entry.get('like_count') or 0
            description = entry.get('description') or ""
            language = entry.get('language')
            thumbnail = entry.get('thumbnail') or ""

            # Skip invalid or short videos
            if not video_id or not title or duration <= 300:
                logging.debug(f"Skipping video {i+1}: invalid data or too short (duration: {duration})")
                continue

            # Filter tutorials
            if "tutorial" not in title.lower() and "tutorial" not in description.lower():
                logging.debug(f"Skipping video {i+1}: not a tutorial")
                continue

            # Filter for English if known
            if language and language.lower() != "en":
                logging.debug(f"Skipping video {i+1}: not English (language: {language})")
                continue

            # Compute fallback thumbnail
            if isinstance(entry.get('thumbnails'), list) and not thumbnail:
                thumbnails = entry.get('thumbnails', [])
                if thumbnails:
                    thumbnail = thumbnails[-1].get('url')

            candidates.append({
                'title': title,
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'thumbnail': thumbnail,
                'duration_mins': round(duration / 60, 1),
                'views': view_count,
                'likes': like_count,
                'score': 0  # Placeholder, to be updated by AI
            })
            logging.debug(f"Added candidate video {i+1}: {title[:50]}...")
            
        except Exception as e:
            logging.warning(f"Error processing video entry {i+1}: {e}")
            continue

    logging.info(f"Processed {len(candidates)} candidate videos")

    if not candidates:
        logging.warning("No candidate videos found after filtering")
        return []

    # Try AI-based scoring, fallback to view-based ranking if AI is unavailable
    try:
        ai_classifier = load_classifier()
        if ai_classifier:
            logging.info("Using AI classifier for video scoring")
            # AI-based scoring using zero-shot classification
            titles = [video['title'] for video in candidates]
            results = ai_classifier(titles, candidate_labels=[topic], multi_label=False)

            for i, video in enumerate(candidates):
                video['score'] = results[i]['scores'][0]  # confidence for the topic

            # Final ranking: AI relevance score × log(views+1)
            from math import log
            for video in candidates:
                video['final_score'] = video['score'] * log(video['views'] + 1)
        else:
            logging.info("AI classifier not available, using view-based ranking")
            # Fallback: use view count for ranking
            from math import log
            for video in candidates:
                video['score'] = 0.5  # Default score
                video['final_score'] = log(video['views'] + 1)
    except Exception as e:
        logging.warning(f"AI scoring failed, using fallback ranking: {e}")
        # Fallback: use view count for ranking
        from math import log
        for video in candidates:
            video['score'] = 0.5  # Default score
            video['final_score'] = log(video['views'] + 1)

    top_videos = sorted(candidates, key=lambda x: x['final_score'], reverse=True)[:5]
    logging.info(f"Returning {len(top_videos)} top videos")
    
    # Log the final results for debugging
    for i, video in enumerate(top_videos):
        logging.info(f"Top video {i+1}: {video['title'][:60]}... (score: {video.get('final_score', 0):.2f})")
    
    return top_videos
