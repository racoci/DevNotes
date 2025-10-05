import os
import sys
from youtube_dl import YoutubeDL

def download_video_segment(video_url, start_time, end_time, output_file_name):
    # Convert start and end times from seconds to hh:mm:ss format
    start_time = str(int(start_time) // 3600).zfill(2) + ':' + str((int(start_time) % 3600) // 60).zfill(2) + ':' + str(int(start_time) % 60).zfill(2)
    end_time = str(int(end_time) // 3600).zfill(2) + ':' + str((int(end_time) % 3600) // 60).zfill(2) + ':' + str(int(end_time) % 60).zfill(2)

    # Set up youtube-dl options
    ydl_opts = {
        'format': 'bestvideo',
        # Specify the external downloader and arguments for ffmpeg
        'external_downloader': 'ffmpeg',
        'external_downloader_args': ['-ss', start_time, '-to', end_time],
    }

    # Download the video using youtube-dl
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # The downloaded file will be saved in the current directory with the video's title.
    # Rename the file to the specified output file name
    os.rename('downloaded_video.mp4', output_file_name)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py VIDEO_URL START_TIME_SECONDS END_TIME_SECONDS OUTPUT_FILE_NAME")
        sys.exit(1)

    # Command line arguments
    video_url = sys.argv[1]
    start_time_seconds = sys.argv[2]
    end_time_seconds = sys.argv[3]
    output_file_name = sys.argv[4]

    download_video_segment(video_url, start_time_seconds, end_time_seconds, output_file_name)
