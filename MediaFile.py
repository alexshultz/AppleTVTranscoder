import subprocess
import json


class MediaFile:
    """
    Represents a media file, encapsulating properties like file path,
    resolution, bitrate, and transcoding requirements.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.resolution = self.get_resolution()
        self.bitrate = self.get_bitrate()
        self.needs_downscaling = self.determine_downscaling()

    def run_ffprobe(self, command):
        """
        Utility method to run ffprobe commands and return the parsed JSON output.
        """
        result = subprocess.run(command, text=True, capture_output=True)
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            raise Exception("ffprobe output was not JSON")

    def get_original_codec(self):
        """
        Uses ffprobe to determine the codec of the original video file.
        """
        command = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_streams', '-select_streams', 'v:0', self.file_path
        ]
        output = self.run_ffprobe(command)
        codec_name = output['streams'][0]['codec_name']
        return codec_name

    def get_resolution(self):
        """
        Use ffprobe to determine resolution.
        Returns a tuple (width, height).
        """
        command = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "json", self.file_path
        ]
        output = self.run_ffprobe(command)
        width = output['streams'][0]['width']
        height = output['streams'][0]['height']
        return (width, height)

    def get_bitrate(self) -> int:
        """
        This method determines the bitrate in kilobits per second using ffprobe.
        """
        ffprobe_command = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "format=bit_rate",
                "-of", "json", self.file_path
            ]
        ffprobe_output = self.run_ffprobe(ffprobe_command)
        bitrate_kbps = int(ffprobe_output['format']['bit_rate']) // 1000
        return bitrate_kbps

    def determine_downscaling(self):
        """
        Determine if downscaling is necessary based on resolution.
        """
        return self.resolution[0] > 1920 or self.resolution[1] > 1080
