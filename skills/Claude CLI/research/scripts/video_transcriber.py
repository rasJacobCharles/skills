#!/usr/bin/env python3
import sys
import re
import argparse
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """
    Extracts the video ID from various YouTube URL formats.
    """
    parsed_url = urlparse(url)
    
    # 1. Standard youtube.com/watch?v=VIDEO_ID
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
        if parsed_url.path == '/watch':
            query = parse_qs(parsed_url.query)
            return query.get('v', [None])[0]
        # 2. youtube.com/shorts/VIDEO_ID
        elif parsed_url.path.startswith('/shorts/'):
            return parsed_url.path.split('/')[2]
        # 3. youtube.com/embed/VIDEO_ID
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
            
    # 4. youtu.be/VIDEO_ID
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path.strip('/')
        
    return None

def format_timestamp(seconds):
    """
    Converts seconds (float) to HH:MM:SS format or MM:SS format.
    """
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def get_youtube_transcript(video_id):
    """
    Fetches the transcript using youtube-transcript-api.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        return None, "Error: 'youtube-transcript-api' is not installed in the virtual environment."
        
    try:
        # Get transcript (automatically tries manual and auto-generated)
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        formatted_lines = []
        for entry in transcript_list:
            timestamp = format_timestamp(entry['start'])
            text = entry['text'].strip()
            formatted_lines.append(f"[{timestamp}] {text}")
            
        return "\n".join(formatted_lines), None
    except Exception as e:
        return None, f"Failed to retrieve YouTube transcript: {str(e)}"

def transcribe_local_file(file_path):
    """
    Placeholder/stub for local video transcribing.
    Requires external libraries (ffmpeg, whisper/speech_recognition) which may not be present.
    """
    try:
        import whisper
        print(f"Whisper found. Transcribing local file: {file_path}...")
        model = whisper.load_model("base")
        result = model.transcribe(file_path)
        
        formatted_lines = []
        for segment in result.get('segments', []):
            timestamp = format_timestamp(segment['start'])
            text = segment['text'].strip()
            formatted_lines.append(f"[{timestamp}] {text}")
            
        return "\n".join(formatted_lines), None
    except ImportError:
        return None, "Local video transcription requires 'openai-whisper' python library. Please run: pip install openai-whisper"
    except Exception as e:
        return None, f"Error transcribing local file: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Extract transcript from YouTube URL or local video.")
    parser.add_argument("--url", help="YouTube URL to transcribe")
    parser.add_argument("--file", help="Local video or audio file to transcribe")
    parser.add_argument("--output", required=True, help="Path to save the output markdown file")
    
    args = parser.parse_args()
    
    transcript = None
    err = None
    
    if args.url:
        video_id = extract_video_id(args.url)
        if not video_id:
            print(f"Error: Could not parse YouTube video ID from URL: {args.url}", file=sys.stderr)
            sys.exit(1)
        print(f"Fetching transcript for YouTube video ID: {video_id}...")
        transcript, err = get_youtube_transcript(video_id)
    elif args.file:
        print(f"Transcribing local file: {args.file}...")
        transcript, err = transcribe_local_file(args.file)
    else:
        print("Error: You must provide either --url or --file", file=sys.stderr)
        sys.exit(1)
        
    if err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
        
    # Write to output file
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f"# Transcript\n\n")
            if args.url:
                f.write(f"**Source:** {args.url}\n\n")
            else:
                f.write(f"**Source File:** {args.file}\n\n")
            f.write(transcript)
            f.write("\n")
        print(f"Transcript written to {args.output}")
    except Exception as e:
        print(f"Error writing to output file: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
