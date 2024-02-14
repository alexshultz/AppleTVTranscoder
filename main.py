# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import argparse
import subprocess
import os
from ResourceManager import ResourceManager
from MediaFile import MediaFile
from TranscodingQueue import TranscodingQueue
from TranscodingJob import TranscodingJob
from Logger import Logger


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process videos for transcoding.')
    parser.add_argument('--input', help='Path to the input video file', required=True)
    parser.add_argument('--output', help='Path to the output video file', required=True)
    return parser.parse_args()


def get_video_metadata(file_path):
    # Example of using ffprobe to get video metadata from Python
    command = ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height,codec_name", "-of", "default=noprint_wrappers=1", file_path]
    result = subprocess.run(command, text=True, capture_output=True)
    return result.stdout


def get_config_from_environment():
    nas_path = os.getenv("NAS_PATH", "/Volumes/Plex/Transcode")
    return nas_path

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = parse_arguments()
    video_file = MediaFile(args.input)
    # Initialize the transcoding queue and resource manager
    transcoding_queue = TranscodingQueue()
    resource_manager = ResourceManager()

    # Example: Add a new media file to the queue
    media_file = MediaFile("/path/to/video.mp4")
    transcoding_queue.add_to_queue(media_file)

    # Process the queue
    while True:
        if resource_manager.check_resources():
            next_media_file = transcoding_queue.get_next_media_file()
            if next_media_file:
                job = TranscodingJob(next_media_file)
                job.execute()
                Logger.log(f"Transcoding completed for {next_media_file.file_path}")
            else:
                Logger.log("No more files to process.")
                break
        else:
            Logger.log("Insufficient resources. Waiting...")
            # Implement waiting logic or break

    # Assume get_video_metadata() or other methods might update video_file properties
    print(f"Transcoding completed: {args.output}")
