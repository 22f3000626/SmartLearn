from yt_dlp import YoutubeDL
from transformers import pipeline

# Load zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def search_youtube(topic):
    query = f"ytsearch20:{topic} tutorial -shorts"
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': False,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        entries = info.get('entries', [])

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

    # AI-based scoring using zero-shot classification
    titles = [video['title'] for video in candidates]
    results = classifier(titles, candidate_labels=[topic], multi_label=False)

    for i, video in enumerate(candidates):
        video['score'] = results[i]['scores'][0]  # confidence for the topic

    # Final ranking: AI relevance score × log(views+1)
    from math import log
    for video in candidates:
        video['final_score'] = video['score'] * log(video['views'] + 1)

    top_videos = sorted(candidates, key=lambda x: x['final_score'], reverse=True)[:5]
    return top_videos
