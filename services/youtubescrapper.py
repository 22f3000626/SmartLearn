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
    query = f"ytsearch20:{topic} tutorial -shorts"
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': False,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            entries = info.get('entries', [])
    except Exception as e:
        logging.error(f"YouTube search failed: {e}")
        return []

    candidates = []
    for entry in entries:
        title = entry.get('title')
        video_id = entry.get('id')
        duration = entry.get('duration', 0)
        view_count = entry.get('view_count') or 0
        like_count = entry.get('like_count') or 0
        description = entry.get('description') or ""
        language = entry.get('language')
        thumbnail = entry.get('thumbnail') or ""

        # Skip invalid or short videos
        if not video_id or not title or duration <= 300:
            continue

        # Filter tutorials
        if "tutorial" not in title.lower() and "tutorial" not in description.lower():
            continue

        # Filter for English if known
        if language and language.lower() != "en":
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

    if not candidates:
        return []

    # Try AI-based scoring, fallback to view-based ranking if AI is unavailable
    try:
        ai_classifier = load_classifier()
        if ai_classifier:
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
    return top_videos
